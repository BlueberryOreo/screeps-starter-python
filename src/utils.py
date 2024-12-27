from defs import *

from creeps_design import ROLES
import logger

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')

dx = [0, 1, 0, -1, 1, 1, -1, -1]
dy = [-1, 0, 1, 0, -1, 1, 1, -1]


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

def get_source_pos(source: Source):
    source_pos = source.pos
    # logger.info("Source: {}, Source pos: {}".format(source, source_pos))
    for i in range(8):
        tmp = __new__(RoomPosition(source_pos.x + dx[i], source_pos.y + dy[i], source_pos.roomName))
        if source.room.getTerrain().get(tmp.x, tmp.y) != TERRAIN_MASK_WALL:
            source_pos = tmp
            for creep in source.room.find(FIND_MY_CREEPS):
                if creep.pos.isEqualTo(tmp):
                    continue
            break
    return source_pos

def waiting(creep: Creep, last_pos: RoomPosition, waiting_time: int = 150):
    # logger.info("[{}] Checking waiting. last_pos: {}, current_pos: {}".format(creep.name, last_pos, creep.pos))
    if not last_pos:
        creep.memory.waiting = 0
        return False
    
    if creep.pos.x == last_pos.x and creep.pos.y == last_pos.y:
        if creep.memory.waiting:
            creep.memory.waiting += 1
        else:
            creep.memory.waiting = 1
        
        if creep.memory.waiting > waiting_time:
            logger.info("[{}] Waiting for {} ticks.".format(creep.name, waiting_time))
            creep.memory.waiting = 0
            return True
    else:
        creep.memory.waiting = 0
    return False