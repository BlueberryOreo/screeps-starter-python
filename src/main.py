# defs is a package which claims to export all constants and some JavaScript objects, but in reality does
#  nothing. This is useful mainly when using an editor like PyCharm, so that it 'knows' that things like Object, Creep,
#  Game, etc. do exist.
from defs import *

from garbage_collector import collect_garbage
from creep_creator import *
from harvester_controller import run_harvester
from upgrader_controller import run_upgrader
from builder_controller import run_builder

import logger
from utils import *
from status import *

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

    # Collect garbage
    collect_garbage()

    # Run each creep
    for name in Object.keys(Game.creeps):
        creep = Game.creeps[name]
        if creep.memory.role == ROLE_HARVESTER:
            run_harvester(creep)
        # elif creep.memory.role == ROLE_UPGRADER:
        #     run_upgrader(creep)
        # elif creep.memory.role == ROLE_BUILDER:
        #     run_builder(creep)
        # elif creep.memory.role == ROLE_REPAIRER:
        #     run_repairer(creep)
        # elif creep.memory.role == ROLE_WALL_REPAIRER:
        #     run_wall_repairer(creep)

    # Run each spawn
    for name in Object.keys(Game.spawns):
        spawn = Game.spawns[name]
        if not spawn.spawning:
            # Get the number of our creeps in the room.
            num_creeps = count_creeps(spawn)

            # If there are no creeps, spawn a creep once energy is at 250 or more
            if num_creeps[ROLE_HARVESTER] < 10 and spawn.room.energyAvailable >= 250:
                create_creep(ROLE_HARVESTER, spawn, [WORK, CARRY, MOVE, MOVE])
            # elif num_creeps[ROLE_UPGRADER] < 2 and spawn.room.energyAvailable >= 250:
            #     create_creep(ROLE_UPGRADER, spawn, [WORK, CARRY, MOVE, MOVE])
            
            # if spawn.room.energyAvailable >= 300 and spawn.room.controller.level >= 2 and num_creeps[ROLE_BUILDER] < 4:
            #     create_creep(ROLE_BUILDER, spawn, [WORK, CARRY, MOVE, MOVE])


module.exports.loop = main
