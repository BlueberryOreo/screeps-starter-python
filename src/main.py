# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
from defs import *

from garbage_collector import collect_garbage
from creep_creator import *
from harvester_controller import run_harvester
from upgrader_controller import run_upgrader
from builder_controller import run_builder
from attacker_controller import run_attacker
from repairer_controller import run_repairer
from carrier_controller import run_carrier

from tower_controller import run_tower

import logger
from utils import *
from status import *
from creeps_design import *

# These are currently required for Transcrypt in order to use the following names in JavaScript.
# Without the 'noalias' pragma, each of the following would be translated into something like 'py_Infinity' or
#  'py_keys' in the output file.
__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def main():
    """
    Main game logic loop.
    """

    # Set creep roles
    harvester = HARVESTER_LEVEL4
    upgrader = UPGRADER_LEVEL3
    builder = BUILDER_LEVEL3
    repairer = REPAIRER_LEVEL3
    attacker = BASE_ATTACKER
    carrier = CARRIER_LEVEL1

    # Collect garbage
    collect_garbage()

    # Run each spawn
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        
        for tower in spawn.room.find(FIND_MY_STRUCTURES, {"filter": lambda s: s.structureType == STRUCTURE_TOWER}):
            run_tower(tower)

        num_creeps = count_creeps(spawn.room)

        if not spawn.spawning:
            # Get the number of our creeps in the room.

            # If there are enemies in the room, then create a attacker
            if spawn.room.find(FIND_HOSTILE_CREEPS).length > 0:
                if num_creeps[ROLE_ATTACKER] < 5 and spawn.room.energyAvailable >= 300:
                    create_creep(ROLE_ATTACKER, spawn, attacker)
                    continue
            
            if num_creeps[ROLE_CARRIER] < 2:
                cost = count_cost(carrier)
                if spawn.room.energyAvailable >= cost:
                    create_creep(ROLE_CARRIER, spawn, carrier)
                    continue

            if num_creeps[ROLE_HARVESTER] < 1:
                cost = count_cost(HARVESTER_LEVEL1)
                if spawn.room.energyAvailable >= cost:
                    create_creep(ROLE_HARVESTER, spawn, HARVESTER_LEVEL1)
                    continue
                    
            if num_creeps[ROLE_HARVESTER] < 2:
                cost = count_cost(harvester)
                if spawn.room.energyAvailable >= cost:
                    create_creep(ROLE_HARVESTER, spawn, harvester)
                    continue
            else:

                if num_creeps[ROLE_CARRIER] < 4:
                    cost = count_cost(carrier)
                    if spawn.room.energyAvailable >= cost:
                        create_creep(ROLE_CARRIER, spawn, carrier)
                        continue
            
                if Memory.dismantle_type:
                    # If there is anything to dismantle
                    if num_creeps[ROLE_HARVESTER] < 3:
                        cost = count_cost(DISMANTLER)
                        if spawn.room.energyAvailable >= cost:
                            creep_memory = {'dismantle_type': Memory.dismantle_type}
                            create_creep(ROLE_HARVESTER, spawn, DISMANTLER, creep_memory)
                            continue
                
                if spawn.room.find(FIND_STRUCTURES, {"filter": lambda s: s.hits < s.hitsMax * 0.5}).length > 0:
                    if num_creeps[ROLE_REPAIRER] < 4:
                        cost = count_cost(repairer)
                        if spawn.room.energyAvailable >= cost:
                            create_creep(ROLE_REPAIRER, spawn, repairer)
                            continue

                if num_creeps[ROLE_UPGRADER] < 8:
                    cost = count_cost(upgrader)
                    if spawn.room.energyAvailable >= cost:
                        create_creep(ROLE_UPGRADER, spawn, upgrader)
                        continue
                    # create_creep(ROLE_UPGRADER, spawn, BASE_UPGRADER)
                
                if spawn.room.find(FIND_CONSTRUCTION_SITES).length > 0:
                    if num_creeps[ROLE_BUILDER] < 4:
                        cost = count_cost(builder)
                        if spawn.room.energyAvailable >= cost:
                            create_creep(ROLE_BUILDER, spawn, builder)
                            continue
                    # create_creep(ROLE_BUILDER, spawn, BASE_BUILDER)
                
                    # create_creep(ROLE_REPAIRER, spawn, BASE_REPAIRER)
                
            # if num_creeps[ROLE_REPAIRER] < 4:
            #     cost = count_cost(REPAIRER_LEVEL1)
            #     if spawn.room.energyAvailable >= cost:
            #         create_creep(ROLE_REPAIRER, spawn, REPAIRER_LEVEL1)
            #         continue
            #     create_creep(ROLE_REPAIRER, spawn, REPAIRER_LEVEL1)
    
        # Run each creep
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        # creep.suicide()
        # continue
        if num_creeps[ROLE_HARVESTER] >= 2:
            # Turn back to the original role
            if creep.memory.last_role:
                del creep.memory.path_to
                del creep.memory.path_back
                del creep.memory.source_id
                del creep.memory.target_id
                creep.memory.role = creep.memory.last_role
                del creep.memory.last_role
                creep.memory.status = S_FINDINGWAY

        if creep.memory.role == ROLE_HARVESTER:
            run_harvester(creep)
        elif creep.memory.role == ROLE_CARRIER:
            run_carrier(creep)
        elif creep.memory.role == ROLE_ATTACKER:
            run_attacker(creep)
        elif creep.memory.role == ROLE_REPAIRER:
            run_repairer(creep)
        elif num_creeps[ROLE_HARVESTER] >= 2 and num_creeps[ROLE_CARRIER] > 0:
            if creep.memory.role == ROLE_UPGRADER:
                run_upgrader(creep)
            elif creep.memory.role == ROLE_BUILDER:
                run_builder(creep)
            else:
                logger.warning("Unexpected role: {}".format(creep.memory.role))
                logger.warning("Suicide")
                creep.suicide()
                continue
        else:
            # If there isn't enough harvester or carrier, then all the creep should become a carrier to transfer there energy to the spawns and extentions
            # if creep.store.getUsedCapacity(RESOURCE_ENERGY):
            creep.memory.last_role = creep.memory.role
            creep.memory.role = ROLE_CARRIER
            del creep.memory.path_to
            del creep.memory.path_back
            del creep.memory.source_id
            del creep.memory.target_id
            creep.memory.status = S_FINDINGWAY

module.exports.loop = main
