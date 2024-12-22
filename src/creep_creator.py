from defs import *
from datetime import datetime

import logger
from harvester_controller import create_harvester

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


ROLE_HARVESTER = 'harvester'
ROLE_UPGRADER = 'upgrader'
ROLE_BUILDER = 'builder'
ROLE_REPAIRER = 'repairer'
ROLE_WALL_REPAIRER = 'wall_repairer'

ROLES = [
    ROLE_HARVESTER, 
    ROLE_UPGRADER, 
    ROLE_BUILDER, 
    ROLE_REPAIRER, 
    ROLE_WALL_REPAIRER
]

def create_creep(role: str, spawn: StructureSpawn, components: list, memory: dict):
    """
        Create a creep.
    """
    if role == ROLE_HARVESTER:
        # time = datetime.now().strftime("%Y%m%d%H%M%S")
        time = str(Game.time)
        return create_harvester(ROLE_HARVESTER + time, spawn, components, memory)
    else:
        logger.warning(f"Unimplemented role {role}.")
        return None

def create_rnd_role():
    pass