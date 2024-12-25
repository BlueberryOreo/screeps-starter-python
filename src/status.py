from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

S_IDEL = "idel"
S_MOVE = "move"
S_WORK = "work"
S_TRANSFER = "transfer"
S_WITHDRAW = "withdraw"
S_BUILD = "build"
S_REPAIR = "repair"
S_UPGRADE = "upgrade"
S_ATTACK = "attack"
S_FINDINGWAY = "findingway"
S_DEAD = "dead"

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