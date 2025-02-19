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
            # creep.memory.role = _.sample([ROLE_UPGRADER, ROLE_REPAIRER])
            creep.memory.role = ROLE_REPAIRER
            logger.info("[{}] Role changed to {}.".format(creep.name, creep.memory.role))
            del creep.memory.path_to
            del creep.memory.path_back
            return

    if creep.memory.status == S_FINDINGWAY:
        if not creep.memory.start or not creep.memory.path_to or not creep.memory.path_back:
            # if creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0.5 * s.store.getCapacity(RESOURCE_ENERGY)}).length > 0:
            source = _.sortBy(creep.room.find(FIND_STRUCTURES, {'filter': lambda s: (s.structureType == STRUCTURE_CONTAINER or s.structureType == STRUCTURE_STORAGE) and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0}),
                              lambda s: s.store.getFreeCapacity(RESOURCE_ENERGY) / s.store.getCapacity(RESOURCE_ENERGY))[0]
            # else:
                # source = _.sample(creep.room.find(FIND_SOURCES))
            
            target = creep.room.find(FIND_CONSTRUCTION_SITES)
            if target.length == 0:
                creep.memory.status = S_IDEL
                return
            
            target = _.sortBy(target, lambda t: t.progressTotal - t.progress)[0] # Find the construction site with the most progress.

            find_path(creep, source, target)

            creep.memory.source_id = source.id
            creep.memory.target_id = target.id
        
        move_to_start(creep)

    if creep.memory.status == S_MOVE:
        creep.memory.status = worker_move(creep)
        
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
