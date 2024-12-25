from defs import *
import logger

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
    # If we're empty, stop upgrading and remove the saved source
    if creep.memory.upgrading and creep.carry.energy <= 0:
        creep.memory.upgrading = False
        del creep.memory.controller
    # If we're full, stop filling and remove the saved target
    elif not creep.memory.upgrading and creep.store.getFreeCapacity() <= 0:
        creep.memory.upgrading = True
        del creep.memory.target
    
    if creep.memory.upgrading:
        # If we have a saved controller, use it
        if creep.memory.controller:
            controller = Game.getObjectById(creep.memory.controller)
        else:
            # Get a random new controller and save it
            controller = creep.room.controller
            creep.memory.controller = controller.id
        
        # If we're near the controller, upgrade it - otherwise, move to it.
        if creep.pos.inRangeTo(controller, 3):
            result = creep.upgradeController(controller)
            if result != OK:
                logger.warning("[{}] Unknown result from creep.upgradeController({}): {}".format(creep.name, controller, result))
        else:
            creep.moveTo(controller)
    else:
        # If we have a saved target, use it
        if creep.memory.target:
            target = Game.getObjectById(creep.memory.target)
        else:
            # Get a random new target and save it
            target = _.sample(creep.room.find(FIND_SOURCES))
            creep.memory.target = target.id
        
        # If we're near the target, harvest it - otherwise, move to it.
        if creep.pos.isNearTo(target):
            result = creep.harvest(target)
            if result != OK:
                logger.warning("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, target, result))
        else:
            creep.moveTo(target)