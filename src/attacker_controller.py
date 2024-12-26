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

def create_attacker(name: str, spawn: StructureSpawn, components: list, memory: dict = None):
    """
        Create a harvester creep.
    """
    logger.info("Creating attacker: " + name + ".")
    if memory:
        memory.role = 'attacker'
    else:
        memory = {'role': 'attacker'}
    res = spawn.createCreep(components, name, memory)
    return res

def run_attacker(creep: Creep):
    """
        Run the attacker creep.
    """
    if creep.memory.status == S_IDEL:
        if creep.spawning:
            return
        creep.memory.status = S_WANDERING
        return
    
    if creep.memory.status == S_WANDERING:
        del creep.memory.target

        if creep.room.find(FIND_FLAGS).length > 0:
            creep.memory.status = S_MOVE_TO_FLAG
            return
        
        if creep.room.find(FIND_HOSTILE_CREEPS).length > 0:
            creep.memory.status = S_FIND_AND_ATTACK
            return
    
    if creep.memory.status == S_MOVE_TO_FLAG:
        flag = creep.room.find(FIND_FLAGS)[0]
        if creep.pos.inRangeTo(flag.pos.x, flag.pos.y, 5):
            creep.memory.status = S_FIND_AND_ATTACK
            return
        creep.moveTo(flag.pos.x, flag.pos.y)
        return
    
    if creep.memory.status == S_FIND_AND_ATTACK:
        if not creep.memory.target:
            target = creep.pos.findClosestByPath(FIND_HOSTILE_CREEPS)
            if target:
                creep.memory.target = target.id
        else:
            target = Game.getObjectById(creep.memory.target)

        if not target:
            creep.memory.status = S_WANDERING
            return
        logger.info("Attacking target: " + target + " " + creep.attack(target))
        if creep.attack(target) == ERR_NOT_IN_RANGE:
            creep.moveTo(target)
        return
    
    # if creep.memory.status == S_MOVE_TO_FLAG:
    #     flag = creep.room.find(FIND_FLAGS)[0]
    #     if not flag:
    #         creep.memory.status = S_WANDERING
    #         return
        
    #     if creep.pos.inRangeTo(flag.pos.x, flag.pos.y, 5):
    #         creep.memory.status = S_FIND_AND_ATTACK
    #         return
    #     creep.moveTo(flag.pos.x, flag.pos.y)
    #     return
    
    # if creep.memory.status == S_ATTACK:
    #     if not creep.memory.target:
    #         target = creep.pos.findInRange(FIND_HOSTILE_CREEPS, 4)
    #         if target:
    #             creep.memory.target = target.id
    #     else:
    #         target = Game.getObjectById(creep.memory.target)

    #     if not target:
    #         creep.memory.status = S_WANDERING
    #         return
    #     if creep.attack(target) == ERR_NOT_IN_RANGE:
    #         creep.moveTo(target)
    #     return