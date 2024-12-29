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
    
    if waiting(creep, creep.memory.last_pos):
        del creep.memory.path_to
        del creep.memory.path_back
        logger.info("[{}] Crashed. Trying to find a new path.".format(creep.name))
        creep.memory.status = S_FINDINGWAY

    if creep.memory.status == S_IDEL:
        if creep.spawning:
            return
        creep.memory.status = S_FINDINGWAY

    if creep.memory.status == S_FINDINGWAY:
        if not creep.memory.path_to or not creep.memory.path_back or not creep.memory.source_id:
            source = None

            if creep.memory.dismantle_type:
                sources = creep.room.find(FIND_STRUCTURES, {'filter': lambda s: s.structureType == creep.memory.dismantle_type})
                # source = _.sortBy(sources, lambda s: s.hits / s.hitsMax)[0] # find the structure with the lowest hits
                source = _.sample(sources)
            
            if not creep.memory.dismantle_type or not source:
                source = _.sample(creep.room.find(FIND_SOURCES))
                if not source:
                    logger.info("[{}] No source found.".format(creep.name))
                    return S_IDEL
                if creep.memory.dismantle_type:
                    del Memory.dismantle_type
                    del creep.memory.dismantle_type
            # spawn = _.sample(creep.room.find(FIND_MY_SPAWNS))
            if creep.memory.dismantle_type:
                targets = _.filter(creep.room.find(FIND_STRUCTURES), 
                                #    lambda s: (s.structureType == STRUCTURE_SPAWN or s.structureType == STRUCTURE_CONTAINER) and s.store.getFreeCapacity(RESOURCE_ENERGY) > 0
                                lambda s: s.structureType == STRUCTURE_CONTAINER and s.store.getFreeCapacity(RESOURCE_ENERGY) > 0
                                                # or ((s.structureType == STRUCTURE_SPAWN or s.structureType == STRUCTURE_EXTENSION) and s.store.getFreeCapacity(RESOURCE_ENERGY) > 0)
                                )
            else:
                # Find the container beside the source.
                targets = []
                for i in range(8):
                    tmp_x = source.pos.x + dx[i]
                    tmp_y = source.pos.y + dy[i]
                    pos = __new__(RoomPosition(tmp_x, tmp_y, creep.room.name))
                    targets = pos.look()
                    if targets.length > 0:
                        flag = True
                        free_capacity = 0
                        for target in targets:
                            if target.type == "creep":
                                flag = False
                                break
                                
                            if target.type == "structure" and target.structure.structureType == STRUCTURE_CONTAINER:
                                free_capacity += target.structure.store.getFreeCapacity(RESOURCE_ENERGY)
                        if free_capacity <= 0:
                            flag = False
                        if flag:
                            break
                target = None
                for tmp in targets:
                    if tmp.type == "structure" and tmp.structure.structureType == STRUCTURE_CONTAINER:
                        target = tmp.structure
                        break
                targets = [target]
                
            if targets.length == 0:
                logger.info("[{}] No target found.".format(creep.name))
                creep.memory.role = _.sample([ROLE_BUILDER, ROLE_UPGRADER, ROLE_REPAIRER])
                logger.info("[{}] Role changed to {}.".format(creep.name, creep.memory.role))
                return

            target = _.sample(targets)
            if creep.memory.dismantle_type and creep.store.getFreeCapacity() > 0:
                find_path(creep, target, source)
            else:
                find_path(creep, source, target)

            creep.memory.source_id = source.id
            if creep.memory.dismantle_type:
                creep.memory.target_id = target.id
        
        move_to_start(creep)

    if creep.memory.status == S_MOVE:
        creep.memory.status = worker_move(creep)
        # logger.info("[{}] Status changed to {}.".format(creep.name, creep.memory.status))
    
    if creep.memory.status == S_WORK:
        if creep.memory.dismantle_type:
            creep.memory.status = destroy(creep)
        else:
            creep.memory.status = work(creep)
        # logger.info("[{}] Status changed to {}.".format(creep.name, creep.memory.status))
    
    if creep.memory.status == S_TRANSFER:
        if creep.memory.dismantle_type:
            target = Game.getObjectById(creep.memory.target_id)
        else:
            target = None
            for i in range(8):
                tmp_x = creep.pos.x + dx[i]
                tmp_y = creep.pos.y + dy[i]
                pos = __new__(RoomPosition(tmp_x, tmp_y, creep.room.name))
                target = pos.lookFor(LOOK_STRUCTURES)[0]
                if target and target.structureType == STRUCTURE_CONTAINER and target.store.getFreeCapacity(RESOURCE_ENERGY) > 0:
                    break
            if not target:
                logger.info("[{}] No available target found.".format(creep.name))
                logger.info("[{}] Waiting.".format(creep.name))
                creep.memory.status = S_TRANSFER
                return
        creep.memory.status = transfer(creep, target)

