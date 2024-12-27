from defs import *
import logger

from status import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

BASE_HARVESTER = [WORK, CARRY, MOVE, MOVE] # cost: 250
BASE_UPGRADER = [WORK, CARRY, MOVE, MOVE] # cost: 250
BASE_BUILDER = [WORK, CARRY, MOVE, MOVE]
BASE_ATTACKER = [ATTACK, MOVE, MOVE, MOVE]
BASE_REPAIRER = [WORK, CARRY, MOVE, MOVE]
RANGED_ATTACKER = [RANGED_ATTACK, MOVE, MOVE, MOVE]

MEDIUM_HARVESTER = [WORK, WORK, CARRY, MOVE, MOVE, MOVE] # cost: 400
MEDIUM_UPGRADER = [WORK, WORK, CARRY, MOVE, MOVE, MOVE] # cost: 400
MEDIUM_BUILDER = [WORK, WORK, CARRY, MOVE, MOVE, MOVE] # cost: 400
MEDIUM_REPAIRER = [WORK, WORK, CARRY, MOVE, MOVE, MOVE] # cost: 400
MEDIUM_HARVESTER2 = [WORK, WORK, CARRY, CARRY, MOVE, MOVE, MOVE, MOVE] # cost: 500
CARRIER = [CARRY, CARRY, MOVE, MOVE] # cost: 200

ROLE_HARVESTER = 'harvester'
ROLE_UPGRADER = 'upgrader'
ROLE_BUILDER = 'builder'
ROLE_REPAIRER = 'repairer'
ROLE_ATTACKER = 'attacker'
ROLE_WALL_REPAIRER = 'wall_repairer'
ROLE_CARRIER = 'carrier'

ROLES = [
    ROLE_HARVESTER, 
    ROLE_UPGRADER, 
    ROLE_BUILDER, 
    ROLE_REPAIRER, 
    ROLE_WALL_REPAIRER,
    ROLE_ATTACKER,
    ROLE_CARRIER
]

COMPONENT_COSTS = {
    WORK: 100,
    CARRY: 50,
    MOVE: 50,
    ATTACK: 80,
    RANGED_ATTACK: 150,
    HEAL: 250,
    CLAIM: 600,
    TOUGH: 10
}

def count_cost(components: list):
    return _.sum(components, lambda c: COMPONENT_COSTS[c])