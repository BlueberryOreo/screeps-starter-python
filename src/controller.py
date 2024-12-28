from defs import *
import logger

from status import *
from creeps_design import *
from utils import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

def work(creep: Creep):
    """
        Work.

        :param creep: Creep

        :return: Next status
    """
    target = Game.getObjectById(creep.memory.source_id)
    if not target:
        # creep.memory.status = S_IDEL
        return S_IDEL
    res = creep.harvest(target)
    if res == ERR_INVALID_TARGET or res == ERR_NO_BODYPART:
        res = creep.withdraw(target, RESOURCE_ENERGY)
        
    if res == ERR_NOT_IN_RANGE:
        creep.moveTo(target)
        return creep.memory.status
    
    if res == ERR_NOT_ENOUGH_RESOURCES:
        logger.info("[{}] Source empty.".format(creep.name))
        logger.info("[{}] Resetting path.".format(creep.name))
        del creep.memory.path_to
        del creep.memory.path_back
        del creep.memory.source_id
        return S_FINDINGWAY
    elif res != OK:
        logger.warning("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, target, res))
    if creep.store.getFreeCapacity() <= 0:
        return S_MOVE
    
    return creep.memory.status


def destroy(creep: Creep):
    """
        Destroy.

        :param creep: Creep

        :return: Next status
    """
    target = Game.getObjectById(creep.memory.source_id)
    if not target:
        return S_IDEL
    if target.structureType and creep.memory.dismantle_type and target.structureType != creep.memory.dismantle_type:
        logger.info("[{}] Target {} (type {}) is not a {}.".format(creep.name, target, target.structureType, creep.memory.dismantle_type))
        logger.info("[{}] Resetting path.".format(creep.name))
        del creep.memory.path_to
        del creep.memory.path_back
        return S_FINDINGWAY
    
    res = creep.dismantle(target)
    if res == ERR_NOT_IN_RANGE:
        creep.moveTo(target)
        return creep.memory.status
    if res != OK:
        logger.warning("[{}] Unknown result from creep.dismantle({}): {}".format(creep.name, target, res))
    if creep.store.getFreeCapacity() <= 0:
        return S_MOVE
    
    return creep.memory.status


def transfer(creep: Creep, target):
    # target = Game.getObjectById(creep.memory.target_id)
    if not target:
        return S_IDEL
    result = creep.transfer(target, RESOURCE_ENERGY)
    if result == ERR_FULL:
        logger.info("[{}] Target {} is full.".format(creep.name, target.name))
        logger.info("[{}] Trying to find another target.".format(creep.name))
        del creep.memory.path_to
        del creep.memory.path_back
        del creep.memory.target_id
        return S_FINDINGWAY
    if result == ERR_INVALID_TARGET:
        logger.info("[{}] Target {} invalid.".format(creep.name, target.name))
        logger.info("[{}] Resetting path.".format(creep.name))
        del creep.memory.path_to
        del creep.memory.path_back
        del creep.memory.target_id
        return S_FINDINGWAY
    if result != OK:
        logger.warning("[{}] Unknown result from creep.transfer({}): {}".format(creep.name, target, result))
    if creep.store.getUsedCapacity() <= 0:
        return S_MOVE
    
    return creep.memory.status
    

def worker_move(creep: Creep, th=0.5):
    """
        Move.

        :param creep: Creep

        :return: Next status
    """

    if creep.store.getUsedCapacity() <= th * creep.store.getCapacity():
        target = Game.getObjectById(creep.memory.source_id)
        path = creep.memory.path_to
        if creep.memory.role == ROLE_CARRIER:
            next_status = S_WITHDRAW
        else:
            next_status = S_WORK
    else:
        path = creep.memory.path_back
        if creep.memory.role == ROLE_HARVESTER:
            next_status = S_TRANSFER
            target = Game.getObjectById(creep.memory.target_id)
            if target and target.store.getFreeCapacity(RESOURCE_ENERGY) <= 0:
                logger.info("[{}] Target full, resetting path.".format(creep.name))
                del creep.memory.path_to
                del creep.memory.path_back
                del creep.memory.target_id
                return S_IDEL
        elif creep.memory.role == ROLE_UPGRADER:
            next_status = S_UPGRADE
            target = creep.room.controller
        elif creep.memory.role == ROLE_BUILDER:
            next_status = S_BUILD
            target = Game.getObjectById(creep.memory.target_id)
            if not target or target.progress >= target.progressTotal:
                logger.info("[{}] Target is constructed, resetting path.".format(creep.name))
                del creep.memory.path_to
                del creep.memory.path_back
                del creep.memory.target_id
                return S_IDEL
        elif creep.memory.role == ROLE_REPAIRER:
            next_status = S_REPAIR
            target = Game.getObjectById(creep.memory.target_id)
            if target and target.hits >= target.hitsMax:
                logger.info("[{}] Target is repaired, resetting path.".format(creep.name))
                del creep.memory.path_to
                del creep.memory.path_back
                del creep.memory.target_id
                return S_IDEL
        elif creep.memory.role == ROLE_CARRIER:
            next_status = S_TRANSFER
            target = Game.getObjectById(creep.memory.target_id)
            if target and target.store.getFreeCapacity(RESOURCE_ENERGY) <= 0:
                logger.info("[{}] Target full, resetting path.".format(creep.name))
                del creep.memory.path_to
                del creep.memory.path_back
                del creep.memory.target_id
                return S_IDEL
        else:
            logger.warning("Unknown role: {}.".format(creep.memory.role))
            return S_IDEL
    
    if target is None:
        logger.warning("[{}] No target found. Maybe disappered while moving to it.".format(creep.name))
        logger.info("[{}] Resetting path.".format(creep.name))
        del creep.memory.path_to
        del creep.memory.path_back
        del creep.memory.target_id
        return S_IDEL
    res = move(creep, path, None)
    # logger.info("[{}] Moving to {}, res {}.".format(creep.name, target, res))
    if next_status == S_WORK:
        if creep.pos.isNearTo(target):
            return next_status
    else:
        if next_status == S_TRANSFER or next_status == S_WITHDRAW:
            if creep.pos.isNearTo(target):
                return next_status
        else:
            if creep.pos.inRangeTo(target, 3):
                return next_status
        
    if res != OK and res != ERR_TIRED:
        logger.warning("[{}] Unknown result from creep.moveByPath({}): {}".format(creep.name, path, res))
        logger.info("[{}] Resetting path.".format(creep.name))
        del creep.memory.path_to
        del creep.memory.path_back
        return S_FINDINGWAY
    
    return creep.memory.status