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

def create_carrier(name: str, spawn: StructureSpawn, components: list, memory: dict = None):
    """
        Create a carrier creep.
    """
    logger.info("Creating carrier: " + name + ".")
    if memory:
        memory.role = 'carrier'
    else:
        memory = {'role': 'carrier'}
    
    res = spawn.createCreep(components, name, memory)
    return res

def run_carrier(creep: Creep):
    """
        Run the carrier creep.
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
            source = _.sample(creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0}))
            target = _.sortBy(creep.room.find(FIND_MY_STRUCTURES, {'filter': lambda s: s.structureType != STRUCTURE_RAMPART and s.structureType != STRUCTURE_CONTROLLER and s.store.getFreeCapacity(RESOURCE_ENERGY) > 0}), lambda s: s.store.getUsedCapacity(RESOURCE_ENERGY) / s.store.getCapacity(RESOURCE_ENERGY) * 100)[0]
            if not source:
                creep.memory.status = S_IDEL
                return
            if not target:
                target = source
            creep.memory.source_id = source.id
            creep.memory.target_id = target.id
            find_path(creep, source, target)
        
        move_to_start(creep)
        return

    if creep.memory.status == S_MOVE:
        creep.memory.status = worker_move(creep, 0)
        return
    
    if creep.memory.status == S_WITHDRAW:
        creep.memory.status = work(creep)
        return
    
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
    