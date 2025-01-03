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

def run_link(room: Room):
    for item in LINK_LINK:
        from_pos = item[0]
        to_pos = item[1]
        link_from: StructureLink = room.lookForAt('structure', from_pos[0], from_pos[1])[0]
        link_to: StructureLink = room.lookForAt('structure', to_pos[0], to_pos[1])[0]
        if not link_from:
            logger.warning("Link not found at ({}, {}).".format(from_pos[0], from_pos[1]))
            return
        if not link_to:
            logger.warning("Link not found at ({}, {}).".format(to_pos[0], to_pos[1]))
            return
        if link_from.store.getUsedCapacity(RESOURCE_ENERGY) > 0 and link_to.store.getFreeCapacity(RESOURCE_ENERGY) > 0:
            res = link_from.transferEnergy(link_to)
            if res == OK:
                logger.info("Link transfered from ({}, {}) to ({}, {}).".format(from_pos[0], from_pos[1], to_pos[0], to_pos[1]))
            elif res != ERR_FULL and res != ERR_TIRED:
                logger.warning("Failed to transfer from ({}, {}) to ({}, {}). Error code: {}.".format(from_pos[0], from_pos[1], to_pos[0], to_pos[1], res))
    return
