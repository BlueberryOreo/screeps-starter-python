from defs import *
import logger

from status import *
from controller import *
from utils import *
from creeps_design import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def create_builder(name: str, spawn: StructureSpawn, components: list, memory: dict = None):
    """
        Create a builder creep.
    """
    logger.info("Creating builder: " + name + ".")
    if memory:
        memory.role = 'builder'
    else:
        memory = {'role': 'builder'}
    
    res = spawn.createCreep(components, name, memory)
    return res


def run_builder(creep: Creep):
    
    if waiting(creep, creep.memory.last_pos):
        del creep.memory.path_to
        del creep.memory.path_back
        logger.info("[{}] Crashed. Trying to find a new path.".format(creep.name))
        creep.memory.status = S_FINDINGWAY
        
    if creep.memory.status == S_IDEL:
        if creep.spawning:
            return
        
        if creep.room.find(FIND_CONSTRUCTION_SITES).length > 0:
            creep.memory.status = S_FINDINGWAY
        else:
            logger.info("[{}] No construction site found.".format(creep.name))
            creep.memory.role = _.sample([ROLE_UPGRADER, ROLE_REPAIRER])
            logger.info("[{}] Role changed to {}.".format(creep.name, creep.memory.role))
            del creep.memory.path_to
            del creep.memory.path_back
        return

    if creep.memory.status == S_FINDINGWAY:
        if not creep.memory.path_to or not creep.memory.path_back:
            if creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0}).length > 0:
                source = _.sample(creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0}))
            else:
                source = _.sample(creep.room.find(FIND_SOURCES))
            target = creep.room.find(FIND_CONSTRUCTION_SITES)
            if target.length == 0:
                creep.memory.status = S_IDEL
                return
            target = _.sortBy(target, lambda t: t.progressTotal - t.progress)[0] # Find the construction site with the most progress.

            find_path(creep, source, target)
            # source_pos = get_source_pos(source)
            # path_to = creep.room.findPath(target.pos, source_pos)
            # # path_to = creep.room.findPath(source.pos, target.pos)
            # start = path_to[path_to.length - 1]
            # goal = path_to[0]
            # path_back = creep.room.findPath(__new__(RoomPosition(start.x, start.y, creep.room.name)),
            #                                 __new__(RoomPosition(goal.x, goal.y, creep.room.name)))
            # find_path = creep.room.findPath(creep.pos, __new__(RoomPosition(goal.x, goal.y, creep.room.name)))
            # creep.memory.start = goal
            # creep.memory.find_path = Room.serializePath(find_path)
            # creep.memory.path_to = Room.serializePath(path_to)
            # creep.memory.path_back = Room.serializePath(path_back)
            # creep.memory.path_to = path_to
            # creep.memory.path_back = path_back

            creep.memory.source_id = source.id
            creep.memory.target_id = target.id
        
        move_to_start(creep)
        return

    if creep.memory.status == S_MOVE:
        creep.memory.status = worker_move(creep)
        return
        # if creep.store.getUsedCapacity() <= 0.5 * creep.store.getCapacity():
        #     target = Game.getObjectById(creep.memory.source_id)
        #     path = creep.memory.path_to
        #     next_status = S_WORK
        # else:
        #     target = Game.getObjectById(creep.memory.target_id)
        #     path = creep.memory.path_back
        #     next_status = S_BUILD
        
        # # last_pos = creep.pos
        
        # res = creep.moveByPath(path)
        # if creep.pos.isNearTo(target):
        #     creep.memory.status = next_status
        #     return
        
        # if res != OK and res != ERR_TIRED:
        #     logger.warning("[{}] Unknown result from creep.moveByPath({}): {}".format(creep.name, path, res))
        #     logger.info("[{}] Resetting path.".format(creep.name))
        #     del creep.memory.path_to
        #     del creep.memory.path_back
        #     creep.memory.status = S_FINDINGWAY
        #     return
        
        # TODO: Avoid the creep in the path.
        # if last_pos.isEqualTo(creep.pos):
        #     if creep.memory.waiting:
        #         creep.memory.waiting += 1
        #     else:
        #         creep.memory.waiting = 1
            
        #     if creep.memory.waiting > 5:
        #         logger.info("[{}] Crash, try to avoid the creep in the path.".format(creep.name))
                
    
    if creep.memory.status == S_WORK:
        creep.memory.status = work(creep)
        return
    
    if creep.memory.status == S_BUILD:
        target = Game.getObjectById(creep.memory.target_id)
        if target is None or (target is not None and target.progress == target.progressTotal):
            creep.memory.status = S_FINDINGWAY
            del creep.memory.path_to
            del creep.memory.path_back
            del creep.memory.target_id
            return
        result = creep.build(target)
        if result != OK:
            logger.warning("[{}] Unknown result from creep.build({}): {}".format(creep.name, target, result))
        if creep.store.getUsedCapacity() <= 0:
            creep.memory.status = S_MOVE
        return
