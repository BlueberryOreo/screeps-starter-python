from defs import *
import logger

from status import *
from creeps_design import *

from controller import *
from utils import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def create_harvester(name: str, spawn: StructureSpawn, components: list, memory: dict = None):
    """
        Create a harvester creep.
    """
    logger.info("Creating harvester: " + name + ".")
    if memory is not None:
        memory.role = ROLE_HARVESTER
    else:
        memory = {'role': ROLE_HARVESTER}
    
    logger.info("memory: {}".format(memory))
    res = spawn.createCreep(components, name, memory)
    return res


def run_harvester(creep: Creep):
    """
        Run the harvester creep.
    """

    if creep.memory.status == S_IDEL:
        if creep.spawning:
            return
        creep.memory.status = S_FINDINGWAY
        return

    if creep.memory.status == S_FINDINGWAY:
        if not creep.memory.path_to or not creep.memory.path_back:
            source = _.sample(creep.room.find(FIND_SOURCES))
            # spawn = _.sample(creep.room.find(FIND_MY_SPAWNS))
            targets = _.filter(creep.room.find(FIND_MY_STRUCTURES), 
                               lambda s: (s.structureType == STRUCTURE_EXTENSION or s.structureType == STRUCTURE_SPAWN or s.structureType == STRUCTURE_CONTAINER) and s.store.getFreeCapacity(RESOURCE_ENERGY) > 0)
            if targets.length == 0:
                logger.info("[{}] No target found.".format(creep.name))
                creep.memory.role = _.sample([ROLE_BUILDER, ROLE_UPGRADER])
                logger.info("[{}] Role changed to {}.".format(creep.name, creep.memory.role))
                return

            target = _.sample(targets)
            source_pos = get_source_pos(source)
            path_to = creep.room.findPath(target.pos, source_pos)
            start = path_to[path_to.length - 1]
            goal = path_to[0]
            path_back = creep.room.findPath(__new__(RoomPosition(start.x, start.y, creep.room.name)),
                                            __new__(RoomPosition(goal.x, goal.y, creep.room.name)))
            find_path = creep.room.findPath(creep.pos, __new__(RoomPosition(goal.x, goal.y, creep.room.name)))
            creep.memory.start = goal
            creep.memory.find_path = Room.serializePath(find_path)
            creep.memory.path_to = Room.serializePath(path_to)
            creep.memory.path_back = Room.serializePath(path_back)
            # creep.memory.path_to = path_to
            # creep.memory.path_back = path_back

            creep.memory.source_id = source.id
            creep.memory.target_id = target.id
        
        if creep.pos.isEqualTo(creep.memory.start.x, creep.memory.start.y):
            creep.memory.status = S_MOVE
            del creep.memory.find_path
            del creep.memory.start
            return
        # creep.moveTo(creep.memory.start.x, creep.memory.start.y)
        last_pos = creep.pos
        creep.moveByPath(creep.memory.find_path)
        if waiting(creep, last_pos):
            del creep.memory.path_to
            del creep.memory.path_back
            del creep.memory.find_path
            creep.memory.status = S_FINDINGWAY
            return
        return

    if creep.memory.status == S_MOVE:
        creep.memory.status = worker_move(creep)
        # logger.info("[{}] Status changed to {}.".format(creep.name, creep.memory.status))
        return
        # if creep.store.getUsedCapacity() <= 0.5 * creep.store.getCapacity():
        #     target = Game.getObjectById(creep.memory.source_id)
        #     path = creep.memory.path_to
        #     next_status = S_WORK
        # else:
        #     target = Game.getObjectById(creep.memory.target_id)
        #     path = creep.memory.path_back
        #     next_status = S_TRANSFER
        
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
    
    if creep.memory.status == S_WORK:
        creep.memory.status = work(creep)
        # logger.info("[{}] Status changed to {}.".format(creep.name, creep.memory.status))
        return
        # source = Game.getObjectById(creep.memory.source_id)
        # result = creep.harvest(source)
        # if result != OK:
        #     logger.warning("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, source, result))
        # if creep.store.getFreeCapacity() <= 0:
        #     creep.memory.status = S_MOVE
        # return
    
    if creep.memory.status == S_TRANSFER:
        target = Game.getObjectById(creep.memory.target_id)
        result = creep.transfer(target, RESOURCE_ENERGY)
        if result == ERR_FULL:
            logger.info("[{}] Target {} is full.".format(creep.name, target.name))
            logger.info("[{}] Trying to find another target.".format(creep.name))
            creep.memory.status = S_FINDINGWAY
            del creep.memory.path_to
            del creep.memory.path_back
            del creep.memory.target_id
            return
        if result != OK:
            logger.warning("[{}] Unknown result from creep.transfer({}): {}".format(creep.name, target, result))
        if creep.store.getUsedCapacity() <= 0:
            creep.memory.status = S_MOVE
        return

