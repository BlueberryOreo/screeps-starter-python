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
            # if creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0.5 * s.store.getCapacity(RESOURCE_ENERGY)}).length > 0:
            source = _.sortBy(creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0}),
                              lambda s: s.store.getFreeCapacity(RESOURCE_ENERGY) + creep.pos.getRangeTo(s))[0]
            # else:
            #     source = _.sample(creep.room.find(FIND_SOURCES))
            target = _.sortBy(creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType != STRUCTURE_WALL and s.structureType != Memory.dismantle_type}), lambda s: s.hits / s.hitsMax)[0]
            # target = _.sample(creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType != STRUCTURE_WALL and s.structureType != Memory.dismantle_type and s.hits < s.hitsMax}))
            if not target or not source:
                logger.warning("[{}] Source or target not found: source: {} target: {}".format(creep.name, source, target))
                creep.memory.status = S_IDEL
                return
            creep.memory.source_id = source.id
            creep.memory.target_id = target.id
            find_path(creep, source, target)

        move_to_start(creep)
    
    if creep.memory.status == S_MOVE:
        creep.memory.status = worker_move(creep)
        
    if creep.memory.status == S_WORK:
        creep.memory.status = work(creep)
    
    if creep.memory.status == S_REPAIR:
        target = Game.getObjectById(creep.memory.target_id)
        if not target or target.hits >= target.hitsMax:
            del creep.memory.target_id
            creep.memory.status = S_IDEL
            return
        res = creep.repair(target)
        if res == ERR_NOT_IN_RANGE:
            creep.moveTo(target)
            return
        if res != OK:
            logger.warning("[{}] Unknown result from creep.repair({}): {}".format(creep.name, target, res))
        if creep.store.getUsedCapacity() <= 0:
            # Find a new target, in case fix the current target forever.
            del creep.memory.path_to
            del creep.memory.path_back
            creep.memory.status = S_FINDINGWAY
