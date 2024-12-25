from defs import *

import logger
from harvester_controller import create_harvester
from upgrader_controller import create_upgrader
from builder_controller import create_builder
from attacker_controller import create_attacker

from status import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def create_creep(role: str, spawn: StructureSpawn, components: list, memory: dict):
    """
        Create a creep.
    """
    time = str(Game.time)
    total_cost = _.sum(components, lambda c: COMPONENT_COSTS[c])
    if total_cost > spawn.room.energyAvailable:
        logger.info("Not enough energy to create creep: {} > {}.".format(total_cost, spawn.room.energyAvailable))
        return None
    
    if memory:
        memory["status"] = S_IDEL
    else:
        memory = {"status": S_IDEL}
    
    if role == ROLE_HARVESTER:
        return create_harvester(ROLE_HARVESTER + time, spawn, components, memory)
    elif role == ROLE_UPGRADER:
        return create_upgrader(ROLE_UPGRADER + time, spawn, components, memory)
    elif role == ROLE_BUILDER:
        return create_builder(ROLE_BUILDER + time, spawn, components, memory)
    elif role == ROLE_ATTACKER:
        return create_attacker(ROLE_ATTACKER + time, spawn, components, memory)
    else:
        logger.warning("Unimplemented role {}.".format(role))
        return None

def create_rnd_role():
    pass