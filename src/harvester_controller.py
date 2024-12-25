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


def create_harvester(name: str, spawn: StructureSpawn, components: list, memory: dict = None):
    """
        Create a harvester creep.
    """
    logger.info("Creating harvester: " + name + ".")
    if memory is not None:
        memory.role = ROLE_HARVESTER
    else:
        memory = {'role': ROLE_HARVESTER}
    
    logger.info("memory: {}".format(memory))
    res = spawn.createCreep(components, name, memory)
    return res


def run_harvester(creep: Creep):
    """
        Run the harvester creep.
    """

    if creep.memory.status == S_IDEL:
        if creep.spawning:
            return
        creep.memory.status = S_FINDINGWAY
        return

    if creep.memory.status == S_FINDINGWAY:
        if not creep.memory.path_to or not creep.memory.path_back:
            source = _.sample(creep.room.find(FIND_SOURCES))
            spawn = _.sample(creep.room.find(FIND_MY_SPAWNS))

            path_to = creep.room.findPath(spawn.pos, source.pos)
            start = path_to[path_to.length - 1]
            goal = path_to[0]
            path_back = creep.room.findPath(__new__(RoomPosition(start.x, start.y, creep.room.name)),
                                            __new__(RoomPosition(goal.x, goal.y, creep.room.name)))
            creep.memory.start = path_to[0]
            creep.memory.path_to = Room.serializePath(path_to)
            creep.memory.path_back = Room.serializePath(path_back)
            # creep.memory.path_to = path_to
            # creep.memory.path_back = path_back

            creep.memory.source_id = source.id
            creep.memory.target_id = spawn.id
        
        if creep.pos.isEqualTo(creep.memory.start.x, creep.memory.start.y):
            creep.memory.status = S_MOVE
            del creep.memory.start
            return
        creep.moveTo(creep.memory.start.x, creep.memory.start.y)
        return

    if creep.memory.status == S_MOVE:
        if creep.store.getFreeCapacity() > 0:
            target = Game.getObjectById(creep.memory.source_id)
            path = creep.memory.path_to
            next_status = S_WORK
        else:
            target = Game.getObjectById(creep.memory.target_id)
            path = creep.memory.path_back
            next_status = S_TRANSFER
        
        res = creep.moveByPath(path)
        if creep.pos.isNearTo(target):
            creep.memory.status = next_status
            return
        
        if res != OK and res != ERR_TIRED:
            logger.warning("[{}] Unknown result from creep.moveByPath({}): {}".format(creep.name, path, res))
            logger.info("[{}] Resetting path.".format(creep.name))
            del creep.memory.path_to
            del creep.memory.path_back
            creep.memory.status = S_FINDINGWAY
            return
    
    if creep.memory.status == S_WORK:
        source = Game.getObjectById(creep.memory.source_id)
        result = creep.harvest(source)
        if result != OK:
            logger.warning("[{}] Unknown result from creep.harvest({}): {}".format(creep.name, source, result))
        if creep.store.getFreeCapacity() <= 0:
            creep.memory.status = S_MOVE
        return
    
    if creep.memory.status == S_TRANSFER:
        target = Game.getObjectById(creep.memory.target_id)
        result = creep.transfer(target, RESOURCE_ENERGY)
        if result != OK:
            logger.warning("[{}] Unknown result from creep.transfer({}): {}".format(creep.name, target, result))
        if creep.store.getUsedCapacity() <= 0:
            creep.memory.status = S_MOVE
        return

