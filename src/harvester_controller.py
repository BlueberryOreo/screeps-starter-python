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


def create_harvester(name: str, spawn: StructureSpawn, components: list, memory: dict = None):
    """
        Create a harvester creep.
    """
    logger.info("Creating harvester: " + name + ".")
    if memory:
        memory.update({'role': 'harvester'})
    else:
        memory = {'role': 'harvester'}
    res = spawn.createCreep(components, name, memory)
    return res


def run_harvester(creep: Creep):
    """
        Run the harvester creep.
    """

    # If we're full, stop filling up and remove the saved source
    if creep.memory.filling and creep.store.getFreeCapacity() <= 0:
        creep.memory.filling = False
        del creep.memory.source
    # If we're empty, start filling again and remove the saved target
    elif not creep.memory.filling and creep.carry.energy <= 0:
        creep.memory.filling = True
        del creep.memory.target

    if creep.memory.filling:
        # If we have a saved source, use it
        if creep.memory.source:
            source = Game.getObjectById(creep.memory.source)
        else:
            # Get a random new source and save it
            source = _.sample(creep.room.find(FIND_SOURCES))
            creep.memory.source = source.id

        # If we're near the source, harvest it - otherwise, move to it.
        if creep.pos.isNearTo(source):
            result = creep.harvest(source)
            if result != OK:
                logger.warning("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, source, result))
        else:
            creep.moveTo(source)
    else:
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            # Get a random new target and save it
            target = _.sample(creep.room.find(FIND_MY_SPAWNS))
            creep.memory.target = target.id
        
        # If we're near the target, transfer energy to it - otherwise, move to it.
        if creep.pos.isNearTo(target):
            result = creep.transfer(target, RESOURCE_ENERGY)
            if result != OK:
                logger.warning("[{}] Unknown result from creep.transfer({}): {}".format(creep.name, target, result))
        else:
            creep.moveTo(target)
