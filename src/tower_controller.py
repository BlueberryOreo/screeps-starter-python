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

def run_tower(tower: StructureTower):
    """
        Run the tower.
    """

    if tower.store.getUsedCapacity(RESOURCE_ENERGY) <= 0:
        return
    
    hostile_creeps = tower.room.find(FIND_HOSTILE_CREEPS)
    if hostile_creeps.length > 0:
        target = _.sortBy(hostile_creeps, lambda c: tower.pos.getRangeTo(c))[0]
        username = target.owner.username
        Game.notify("User {} spotted in room {}.".format(username, tower.room.name))
        res = tower.attack(target)
        if res == OK:
            logger.info("[{}] Attacking: {}.".format(tower, target))
        else:
            logger.warning("[{}] Failed to attack: {}. Error code: {}.".format(tower, target, res))
        return
    
    # damaged_my_structures = tower.room.find(FIND_MY_STRUCTURES, {'filter': lambda s: s.hits < 0.5 * s.hitsMax})
    # damaged_public_structures = tower.room.find(FIND_STRUCTURES, {'filter': lambda s: s.hits < 0.5 * s.hitsMax})
    # if damaged_my_structures.length > 0:
    #     target = _.sortBy(damaged_my_structures, lambda s: s.hits / s.hitsMax)[0]
    #     res = tower.repair(target)
    #     if res != OK:
    #         logger.warning("[{}] Failed to repair: {}. Error code: {}.".format(tower, target, res))
    #     return
    # elif damaged_public_structures.length > 0:
    #     target = _.sortBy(damaged_public_structures, lambda s: s.hits / s.hitsMax)[0]
    #     res = tower.repair(target)
    #     if res == OK:
    #         logger.info("[{}] Repairing: {}.".format(tower, target))
    #     else:
    #         logger.warning("[{}] Failed to repair: {}. Error code: {}.".format(tower, target, res))
    #     return
    
    damaged_creeps = tower.room.find(FIND_MY_CREEPS, {'filter': lambda c: c.hits < c.hitsMax})
    if damaged_creeps.length > 0:
        target = _.sortBy(damaged_creeps, lambda c: c.hits / c.hitsMax)[0]
        res = tower.heal(target)
        if res == OK:
            logger.info("[{}] Healing: {}.".format(tower, target))
        else:
            logger.warning("[{}] Failed to heal: {}. Error code: {}.".format(tower, target, res))
        return
    