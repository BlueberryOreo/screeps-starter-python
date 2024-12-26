from defs import *
import logger

from status import *
from creeps_design import *

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
    if res == ERR_NOT_IN_RANGE:
        creep.moveTo(target)
        return S_WORK
    if creep.store.getFreeCapacity() <= 0:
        return S_MOVE
    return S_WORK

def worker_move(creep: Creep):
    """
        Move.

        :param creep: Creep

        :return: Next status
    """

    if creep.store.getUsedCapacity() <= 0.5 * creep.store.getCapacity():
        target = Game.getObjectById(creep.memory.source_id)
        path = creep.memory.path_to
        next_status = S_WORK
    else:
        path = creep.memory.path_back
        if creep.memory.role == ROLE_HARVESTER:
            next_status = S_TRANSFER
            target = Game.getObjectById(creep.memory.target_id)
        elif creep.memory.role == ROLE_UPGRADER:
            next_status = S_UPGRADE
            target = creep.room.controller
        elif creep.memory.role == ROLE_BUILDER:
            next_status = S_BUILD
            target = Game.getObjectById(creep.memory.target_id)
        elif creep.memory.role == ROLE_REPAIRER:
            next_status = S_REPAIR
            target = Game.getObjectById(creep.memory.target_id)
        else:
            logger.warning("Unknown role: {}.".format(creep.memory.role))
            return S_IDEL
    
    res = creep.moveByPath(path)
    # logger.info("[{}] Moving to {}, res {}.".format(creep.name, target, res))
    if next_status == S_WORK:
        if creep.pos.isNearTo(target):
            return next_status
    else:
        if next_status == S_TRANSFER:
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
    
    return S_MOVE