from defs import *

__pragma__('noalias', 'name')
__pragma__('noalias', 'undefined')
__pragma__('noalias', 'Infinity')
__pragma__('noalias', 'keys')
__pragma__('noalias', 'get')
__pragma__('noalias', 'set')
__pragma__('noalias', 'type')
__pragma__('noalias', 'update')


def info(*msg):
    msg = ' '.join(msg)
    console.log("[INFO]: " + msg)

def error(*msg):
    msg = ' '.join(msg)
    console.log("[ERROR]: " + msg)

def warning(*msg):
    msg = ' '.join(msg)
    console.log("[WARNING]: " + msg)

def debug(*msg):
    msg = ' '.join(msg)
    console.log("[DEBUG]: " + msg)