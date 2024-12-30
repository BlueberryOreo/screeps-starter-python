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
    
    if creep.memory.status == S_FINDINGWAY:
        if not creep.memory.path_to or not creep.memory.path_back or not creep.memory.source_id or not creep.memory.target_id:
            source = _.sortBy(creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0}),
                              lambda s: s.store.getFreeCapacity(RESOURCE_ENERGY))[0]
            unfilled_towers = creep.room.find(FIND_MY_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_TOWER and s.store.getFreeCapacity(RESOURCE_ENERGY) > 0})
            if unfilled_towers.length > 0 and count_creeps(creep.room, ROLE_HARVESTER) > 1:
                target = _.sortBy(unfilled_towers, lambda s: s.store.getUsedCapacity(RESOURCE_ENERGY))[0]
            else:
                target = _.sortBy(creep.room.find(FIND_MY_STRUCTURES, {'filter': lambda s: s.structureType != STRUCTURE_RAMPART and s.structureType != STRUCTURE_CONTROLLER and s.store.getFreeCapacity(RESOURCE_ENERGY) > 0}), lambda s: s.store.getUsedCapacity(RESOURCE_ENERGY) / s.store.getCapacity(RESOURCE_ENERGY) * 100)[0]
            if not source or not target:
                logger.info("[{}] No source or target found.".format(creep.name))
                creep.memory.status = S_IDEL
                return
            creep.memory.source_id = source.id
            creep.memory.target_id = target.id
            find_path(creep, source, target)
        
        move_to_start(creep)

    if creep.memory.status == S_MOVE:
        creep.memory.status = worker_move(creep, 0)
    
    if creep.memory.status == S_WITHDRAW:
        creep.memory.status = work(creep)
    
    if creep.memory.status == S_TRANSFER:
        target = Game.getObjectById(creep.memory.target_id)
        result = creep.transfer(target, RESOURCE_ENERGY)
        if result == ERR_FULL:
            logger.info("[{}] Target {} is full.".format(creep.name, target))
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
    