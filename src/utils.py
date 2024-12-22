from defs import *

from creep_creator import ROLES

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def count_creeps(spawn: StructureSpawn, role: str = None):
    """
        Count the number of creeps in the game.
    """
    if role:
        cnt = _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName and c.memory.role == role)
        res = {
            role: cnt
        }
    else:
        res = {
            k: _.sum(Game.creeps, lambda c: c.pos.roomName == spawn.pos.roomName and c.memory.role == k) for k in ROLES
        }
    return res
