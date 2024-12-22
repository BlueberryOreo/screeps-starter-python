from defs import *
import logger

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def collect_garbage():
    """
    Check and remove the dead creeps from the memory.
    """
    memory = Memory.creeps
    for name in Object.keys(memory):
        # logger.debug(name, Game.creeps[name])
        if not Game.creeps[name]:
            logger.info(f"Removed dead creep {name} from memory.")
            del memory[name]
    
