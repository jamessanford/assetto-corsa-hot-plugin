CLIENT USAGE:

EDIT client_debug.py to have the .py filenames you want to send
EDIT client_debug.py IP address (192.168.1.77)
EDIT hot_app/hot_app.py def pyroserver() IP address (192.168.1.77)

OPEN port 9999 on AC host windows firewall (allow 'ac' incoming connections)

COPY 'hot_app' folder to C:/Program Files/Steam/steamapps/common/assettocorsa/apps/python/
RUN AC
Options -> General -> UI Modules -> Enable 'hot app'
START AC
Make sure the 'hot app' icon is visible on right hand side.
If not, check My Documents/Assetto Corsa/Logs/log.txt and py_log.txt



HOT RELOADING:

# Send local .py files to AC plugin and perform hot-reload
linux% ./client_debug.py send


# Look at recent errors
linux% ./client_debug.py error



CONSOLE EXAMPLES:

# Interactive python prompt with AC client
linux% ./client_debug.py console
>


import sys
sys.modules['hot_app_lib'].data

sys.modules['hot_app'].my_hot_app.local_data

import sim_info
sim_info.info.static.sectorCount

import ac
import acsys
ac.getCarName(0)

dir(ac)
dir(acsys)




HOW THE MAGIC WORKS

The magic is:

hot_app.py
  Attaching pyroserver to port 9999 in a separate thread

hot_app_lib.py
  class HotApp
    self.data
      ^ This dict is kept across hot reloads

hot_app_lib.py
  acUpdate()
    first_update
      reinitialize_app()
        do all your app initialization here.

        for things that can only happen once ever,
        like creating a NEW label, check self.data
        to see if it has already been done.

        for things that can be performed multiple times,
        like setting the SIZE of a label, go ahead and
        just set the size again.
        this lets you change the size of a label on hot reload.

