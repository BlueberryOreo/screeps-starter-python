from defs import *

from creeps_design import *
from status import *
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

def move(creep: Creep, path=None, target=None):
    creep.memory.last_pos = creep.pos
    if path is not None:
        res = creep.moveByPath(path)
    elif target is not None:
        res = creep.moveTo(target)
    else:
        logger.warning("[{}] No path or target to move. path: {}, target: {}".format(creep.name, path, target))
        res = ERR_INVALID_ARGS
    return res

def waiting(creep: Creep, last_pos: RoomPosition, waiting_time: int = 100):
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

def find_path(creep: Creep, source, target):
    if not source:
        logger.warning("[{}] No source found.".format(creep.name))
        creep.memory.status = S_FINDINGWAY
        return
    source_pos = get_source_pos(source)
    if creep.memory.role == ROLE_HARVESTER and not creep.memory.dismantle_type:
        find_path = creep.room.findPath(creep.pos, source_pos)
        creep.memory.start = source_pos
        creep.memory.find_path = Room.serializePath(find_path)
        return
    
    path_to = creep.room.findPath(target.pos, source_pos)
    # path_to = creep.room.findPath(source.pos, target.pos)
    start = path_to[path_to.length - 1]
    goal = path_to[0]
    if not start or not goal:
        logger.warning("[{}] No start or goal found, start: {}, goal: {}, path_to: {}.".format(creep.name, start, goal, path_to))
        logger.warning("[{}] Source: {}, Target: {}".format(creep.name, source, target))
        del creep.memory.path_to
        del creep.memory.path_back
        creep.memory.status = S_FINDINGWAY
        return
    path_back = creep.room.findPath(__new__(RoomPosition(start.x, start.y, creep.room.name)),
                                    __new__(RoomPosition(goal.x, goal.y, creep.room.name)))
    find_path = creep.room.findPath(creep.pos, __new__(RoomPosition(goal.x, goal.y, creep.room.name)))
    creep.memory.start = goal
    creep.memory.find_path = Room.serializePath(find_path)
    creep.memory.path_to = Room.serializePath(path_to)
    creep.memory.path_back = Room.serializePath(path_back)
    
def move_to_start(creep: Creep):
    if not creep.memory.start:
        del creep.memory.path_to
        del creep.memory.path_back
        logger.info("[{}] No start found.".format(creep.name))
        creep.memory.status = S_FINDINGWAY
        return
    if creep.pos.isEqualTo(creep.memory.start.x, creep.memory.start.y):
        creep.memory.status = S_MOVE
        del creep.memory.find_path
        del creep.memory.start
        if creep.memory.role == ROLE_HARVESTER and not creep.memory.dismantle_type:
            del creep.memory.path_to
            del creep.memory.path_back
            creep.memory.status = S_WORK
        return
    # creep.moveTo(creep.memory.start.x, creep.memory.start.y)
    move(creep, creep.memory.find_path, None)
