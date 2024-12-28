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
            if creep.memory.dismentle_type or creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0}).length > 0:
                source = _.sample(creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getUsedCapacity(RESOURCE_ENERGY) > 0}))
            else:
                source = _.sample(creep.room.find(FIND_SOURCES))
            
            if creep.memory.dismentle_type:
                target = creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == creep.memory.dismentle_type})
                if target.length == 0:
                    del creep.memory.dismentle_type
            else:
                target = creep.room.find(FIND_CONSTRUCTION_SITES)
            if target.length == 0:
                creep.memory.status = S_IDEL
                return
            
            if creep.memory.dismentle_type:
                target = _.sortBy(target, lambda t: t.hits)[0] # Find the structure with the least hits.
            else:
                target = _.sortBy(target, lambda t: t.progressTotal - t.progress)[0] # Find the construction site with the most progress.

            find_path(creep, source, target)

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
        if creep.memory.dismentle_type:
            target = Game.getObjectById(creep.memory.source_id)
            creep.memory.status = transfer(creep, target)
        else:
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
        if creep.memory.dismentle_type:
            result = creep.dismantle(target)
        else:
            result = creep.build(target)
        if result != OK:
            logger.warning("[{}] Unknown result from creep.build({}): {}".format(creep.name, target, result))
        
        if creep.memory.dismentle_type:
            if target.hits <= 0:
                logger.info("[{}] Target {} dismentled.".format(creep.name, target))
                if creep.store.getFreeCapacity() <= 0:
                    creep.memory.status = S_MOVE
                else:
                    creep.memory.status = S_FINDINGWAY
                    del creep.memory.path_to
                    del creep.memory.path_back
                    del creep.memory.target_id
        else:
            if creep.store.getUsedCapacity() <= 0:
                creep.memory.status = S_MOVE
        return
