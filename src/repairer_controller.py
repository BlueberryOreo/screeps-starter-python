from defs import *
import logger

from status import *
from creeps_design import *
from controller import *
from utils import get_source_pos

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def create_repairer(name: str, spawn: StructureSpawn, components: list, memory: dict = None):
    """
        Create a repairer creep.
    """
    logger.info("Creating repairer: " + name + ".")
    if memory:
        memory.role = ROLE_REPAIRER
    else:
        memory = {'role': ROLE_REPAIRER}
    res = spawn.createCreep(components, name, memory)
    return res

def run_repairer(creep: Creep):
    """
        Run the repairer creep.
    """

    if creep.memory.status == S_IDEL:
        if creep.spawning:
            return
        creep.memory.status = S_FINDINGWAY
        return
    
    if creep.memory.status == S_FINDINGWAY:
        if not creep.memory.path_to or not creep.memory.path_back:
            source = creep.room.find(FIND_SOURCES) + creep.room.find(FIND_STRUCTURES, {
                'filter': lambda s: s.structureType == STRUCTURE_CONTAINER or s.structureType == STRUCTURE_STORAGE
            })
            source = _.sample(source)
            target = _.sortBy(creep.room.find(FIND_STRUCTURES), lambda s: s.hits / s.hitsMax)[0]
            if not target:
                creep.memory.status = S_IDEL
                return
            creep.memory.source_id = source.id
            creep.memory.target_id = target.id
            source_pos = get_source_pos(source)
            path_to = creep.room.findPath(creep.pos, source_pos)
            start = path_to[path_to.length - 1]
            goal = path_to[0]
            path_back = creep.room.findPath(__new__(RoomPosition(start.x, start.y, creep.room.name)),
                                            __new__(RoomPosition(goal.x, goal.y, creep.room.name)))
            find_path = creep.room.findPath(creep.pos, __new__(RoomPosition(start.x, start.y, creep.room.name)))
            creep.memory.start = start
            creep.memory.find_path = Room.serializePath(find_path)
            creep.memory.path_to = Room.serializePath(path_to)
            creep.memory.path_back = Room.serializePath(path_back)
            return
        else:
            if creep.pos.isEqualTo(creep.memory.start.x, creep.memory.start.y):
                creep.memory.status = S_MOVE
                del creep.memory.find_path
                del creep.memory.start
                return
            creep.moveByPath(creep.memory.find_path)
            return
    
    if creep.memory.status == S_MOVE:
        creep.memory.status = worker_move(creep)
        return
        
    if creep.memory.status == S_WORK:
        creep.memory.status = work(creep)
        return
    
    if creep.memory.status == S_REPAIR:
        target = Game.getObjectById(creep.memory.target_id)
        if not target:
            del creep.memory.target_id
            creep.memory.status = S_IDEL
            return
        res = creep.repair(target)
        if res != OK:
            logger.warning("[{}] Unknown result from creep.repair({}): {}".format(creep.name, target, res))
        if creep.store.getUsedCapacity() <= 0:
            creep.memory.status = S_MOVE
        return
