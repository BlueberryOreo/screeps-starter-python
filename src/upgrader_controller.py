from defs import *
import logger

from status import *
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


def create_upgrader(name: str, spawn: StructureSpawn, components: list, memory: dict = None):
    """
        Create a harvester creep.
    """
    logger.info("Creating upgrader: " + name + ".")
    if memory:
        memory.role = 'upgrader'
    else:
        memory = {'role': 'upgrader'}
    res = spawn.createCreep(components, name, memory)
    return res

def run_upgrader(creep: Creep):
    """
        Run the upgrader creep.
    """
    if waiting(creep, creep.memory.last_pos):
        del creep.memory.path_to
        del creep.memory.path_back
        logger.info("[{}] Crashed. Trying to find a new path.".format(creep.name))
        creep.memory.status = S_FINDINGWAY
    
    if creep.memory.status == S_IDEL:
        if creep.spawning:
            return
        creep.memory.status = S_FINDINGWAY
        return
    
    if creep.memory.status == S_FINDINGWAY:
        if not creep.memory.path_to or not creep.memory.path_back:
            # if creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0}).length > 0:
            #     source = _.sample(creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0}))
            # else:
            source = _.sample(creep.room.find(FIND_SOURCES))
            controller = creep.room.controller

            find_path(creep, source, controller)
            # source_pos = get_source_pos(source)
            # path_to = creep.room.findPath(controller.pos, source_pos)
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
        
        move_to_start(creep)
        return

    if creep.memory.status == S_MOVE:
        creep.memory.status = worker_move(creep)
        # if creep.store.getUsedCapacity() <= 0.5 * creep.store.getCapacity():
        #     target = Game.getObjectById(creep.memory.source_id)
        #     path = creep.memory.path_to
        #     next_status = S_WORK
        # else:
        #     target = creep.room.controller
        #     path = creep.memory.path_back
        #     next_status = S_UPGRADE
        
        # res = creep.moveByPath(path)
        # if next_status == S_WORK:
        #     if creep.pos.isNearTo(target):
        #         creep.memory.status = next_status
        #         return
        # else:
        #     if creep.pos.inRangeTo(target, 3):
        #         creep.memory.status = next_status
        #         return
            
        # if res != OK and res != ERR_TIRED:
        #     logger.warning("[{}] Unknown result from creep.moveByPath({}): {}".format(creep.name, path, res))
        #     logger.info("[{}] Resetting path.".format(creep.name))
        #     del creep.memory.path_to
        #     del creep.memory.path_back
        #     creep.memory.status = S_FINDINGWAY
        #     return
    
    if creep.memory.status == S_WORK:
        creep.memory.status = work(creep)
        return
    #     source = Game.getObjectById(creep.memory.source_id)
    #     result = creep.harvest(source)
    #     if result != OK:
    #         logger.warning("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, source, result))
    #     if creep.store.getFreeCapacity() <= 0:
    #         creep.memory.status = S_MOVE
    #     return
    
    if creep.memory.status == S_UPGRADE:
        target = creep.room.controller
        result = creep.upgradeController(target)
        if result != OK:
            logger.warning("[{}] Unknown result from creep.upgradeController({}): {}".format(creep.name, target, result))
        if creep.store.getUsedCapacity() <= 0:
            creep.memory.status = S_MOVE
        return
