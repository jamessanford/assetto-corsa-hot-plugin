#!/usr/bin/python3

# PYRO_LOGFILE="{stderr}" PYRO_LOGLEVEL=DEBUG

# EDIT the name of your main module here
APP_MODULE = 'hot_app'

# EDIT directory where your app library source files are
APP_LIBDIR = 'hot_app_lib'

# EDIT the modules that should be hot reloaded
SOURCE_FILES = ("sim_info.py", "config.py", "hot_app_lib.py")

import os
import sys
import time

import Pyro4.core
import Pyro4.utils.flame

Pyro4.config.SERIALIZER = "pickle"  # flame requires pickle serializer
Pyro4.config.PICKLE_PROTOCOL_VERSION = 3

def main(args):
  # EDIT your AC host IP address here
  #location = "localhost:9999"
  location = "192.168.1.77:9999"
  flame = Pyro4.core.Proxy("PYRO:%s@%s" % (Pyro4.constants.FLAME_NAME, location))
  #flame._pyroHmacKey = "FOO"
  flame._pyroBind()

  # print something to the remote server output
  #flame.builtin("print")("Hello there, remote server stdout!")

  if len(args) < 2:
    args.append('help')  # you need help

  # remote console
  if args[1] == 'console':
    with flame.console() as console:
      console.interact()
  elif args[1] == 'send':
    # This pauses acUpdate while we reload the module
    flame.evaluate("setattr(sys.modules['%s'], 'has_error', True)" % (APP_MODULE,))
    time.sleep(0.1)  # wait for another frame to pass

    for filename in SOURCE_FILES:
      modulename = filename[:filename.rindex(".py")]
      modulesource = open(os.path.join(APP_LIBDIR, filename)).read()
      flame.sendmodule('.'.join((APP_LIBDIR, modulename)), modulesource)

    # Allow acUpdate to run again
    time.sleep(0.1)
    flame.evaluate("setattr(sys.modules['%s'], 'has_error', False)" % (APP_MODULE,))
  elif args[1] in ('error', 'errors', 'watch'):
    while True:
      logged_errors = flame.evaluate("sys.modules['%s'].logged_errors" % (APP_MODULE,))
#      print(logged_errors)
#      sys.exit(0)
#      delta = flame.module(APP_MODULE)
#      print(list(delta.logged_errors))
#      import code
#      foo = globals().copy()
#      foo.update(locals())
#      code.InteractiveConsole(locals=foo).interact()
      for error in logged_errors:
        print(error)
      if args[1] == 'watch':
        time.sleep(1)
        print()
      else:
        break
  else:
    print("use 'console', 'send', or 'errors' command")
    sys.exit(1)


if __name__ == '__main__':
  main(sys.argv)
