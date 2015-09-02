import ac
import sys
import threading
import time
import traceback

# This is the entry point for the Assetto Corsa API,
# we wrap the API calls with some error checking and farm it
# out to our actual implementation.
#
# This wrapper allows us to replace the hot_app_lib module
# with a new version while AC is running; AC will still call
# the endpoints here but we can switch over to the new module version.

has_error = False
logged_errors = []


def log_error():
  msg = 'Exception: {}\n{}'.format(time.asctime(), traceback.format_exc())
  ac.log(msg)
  ac.console(msg)
  logged_errors.append(msg)


sys.path.insert(0, 'apps/python/hot_app/lib')


try:
  import Pyro4.core
  import Pyro4.utils.flame
except:
  log_error()
  raise


class HotAppData:
  pass

# Important to do this before importing hot_app_lib.
hot_app_data = HotAppData()


try:
  import hot_app_lib.hot_app_lib
except:
  log_error()
  raise

try:
  import encodings.idna
except:
  log_error()


def pyroserver():
  Pyro4.config.SERIALIZER = 'pickle'
  Pyro4.config.PICKLE_PROTOCOL_VERSION = 3
  Pyro4.config.SERIALIZERS_ACCEPTED = set(['pickle'])
  Pyro4.config.SOCK_REUSE = True
  Pyro4.config.DETAILED_TRACEBACK = True
  Pyro4.config.FLAME_ENABLED = True

  try:
    # FIXME: Listening on '' is not working here
    # it listens properly, but the Pyro client then reconnects to localhost
#    daemon = Pyro4.core.Daemon(host='', port=9999)  # FIXME
# EDIT the IP below
    daemon = Pyro4.core.Daemon(host='192.168.1.77', port=9999)  # hot_app
    uri = Pyro4.utils.flame.start(daemon)
    ac.console('uri %s' % uri)
    daemon.requestLoop()
    daemon.close()
  except:
    log_error()
    raise


def acMain(ac_version):
  # DEBUG
  t = threading.Thread(target=pyroserver)
  t.daemon = True
  t.start()

  try:
    hot_app_data.app_id = ac.newApp('hot_app')
    ac.addRenderCallback(hot_app_data.app_id, onRender)

    return hot_app_lib.hot_app_lib.my_hot_app.acMain(ac_version)
  except:
    log_error()
    raise


def acUpdate(delta_t):
  global has_error
  if has_error:
    return
  try:
    hot_app_lib.hot_app_lib.my_hot_app.acUpdate(delta_t)
  except:
    log_error()
    has_error = True


def acShutdown():
  global has_error
  if has_error:
    return
  try:
    hot_app_lib.hot_app_lib.my_hot_app.acShutdown()
  except:
    log_error()
    has_error = True


def onRender(delta_t):
  global has_error
  if has_error:
    return
  try:
    hot_app_lib.hot_app_lib.my_hot_app.onRender(delta_t)
  except:
    log_error()
    has_error = True


def onClick(*args, **kwargs):
  global has_error
  if has_error:
    return
  try:
    hot_app_lib.hot_app_lib.my_hot_app.onClick()
  except:
    log_error()
    has_error = True
