from defs import *
import logger
import random

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
        memory.update({'role': 'builder'})
    else:
        memory = {'role': 'builder'}
    res = spawn.createCreep(components, name, memory)
    return res


def run_builder(creep: Creep):
    if creep.memory.building and creep.store.getUsedCapacity(RESOURCE_ENERGY) <= 0:
        creep.memory.building = False
        del creep.memory.target
    elif not creep.memory.building and creep.store.getFreeCapacity() <= 0:
        creep.memory.building = True
        del creep.memory.target
    
    if creep.memory.building:
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            target = _.sample(creep.room.find(FIND_CONSTRUCTION_SITES))
            if target:
                creep.memory.target = target.id
            else:
                # target = creep.room.controller
                creep.memory.target = None
                return
        
        if creep.pos.inRangeTo(target, 3):
            result = creep.build(target)
            if result != OK:
                logger.warning("[{}] Unknown result from creep.build({}): {}".format(creep.name, target, result))
        else:
            creep.moveTo(target)
    else:
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            target = _.sample(creep.room.find(FIND_SOURCES))
            creep.memory.target = target.id
        
        if creep.pos.isNearTo(target):
            result = creep.harvest(target)
            if result != OK:
                logger.warning("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, target, result))
        else:
            creep.moveTo(target)