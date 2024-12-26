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
RANGED_ATTACKER = [RANGED_ATTACK, MOVE, MOVE, MOVE]

MEDIUM_HARVESTER = [WORK, WORK, CARRY, MOVE, MOVE, MOVE] # cost: 400