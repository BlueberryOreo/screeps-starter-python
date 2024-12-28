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
    
    if creep.memory.status == S_FINDINGWAY:
        if not creep.memory.path_to or not creep.memory.path_back:
            # if creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0}).length > 0:
            #     source = _.sample(creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0}))
            # else:
            source = _.sample(creep.room.find(FIND_SOURCES))
            controller = creep.room.controller

            find_path(creep, source, controller)

            creep.memory.source_id = source.id
        
        move_to_start(creep)

    if creep.memory.status == S_MOVE:
        creep.memory.status = worker_move(creep)
    
    if creep.memory.status == S_WORK:
        creep.memory.status = work(creep)
    
    if creep.memory.status == S_UPGRADE:
        target = creep.room.controller
        result = creep.upgradeController(target)
        if result != OK:
            logger.warning("[{}] Unknown result from creep.upgradeController({}): {}".format(creep.name, target, result))
        if creep.store.getUsedCapacity() <= 0:
            creep.memory.status = S_MOVE
