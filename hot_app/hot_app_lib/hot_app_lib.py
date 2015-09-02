import ac
import acsys
import sys

from hot_app_lib import config
from hot_app_lib import sim_info


class HotApp:
  def __init__(self):
    self.data = sys.modules['hot_app'].hot_app_data
    self.first_update = True
    self.local_frame_count = 0

  def acMain(self, version):
    ac.setTitle(self.data.app_id, "")
    ac.setBackgroundOpacity(self.data.app_id, 0.0)
    ac.drawBorder(self.data.app_id, 0)
    ac.setIconPosition(self.data.app_id, 0, -10000)
    ac.setSize(self.data.app_id, config.APP_WIDTH, config.APP_HEIGHT)

    return 'hot_app'

  def acShutdown(self):
    return

  def reinitialize_app(self):

    # Initialize all 'data' fields we use.
    if not hasattr(self.data, 'frame_count'):
      self.data.frame_count = 0

    # Only create the text label once.
    if not hasattr(self.data, 'banner'):
      self.data.banner = ac.addLabel(self.data.app_id, '')

    # But set the size and positioning every time the app is hot reloaded.
    ac.setPosition(self.data.banner, 0, 0)  # X, Y relative to main app window
    ac.setSize(self.data.banner, config.LABEL_WIDTH, config.LABEL_HEIGHT)

    ac.setFontAlignment(self.data.banner, 'center')
    ac.setFontSize(self.data.banner, config.FONT_SIZE)
    ac.setFontColor(self.data.banner, 0.945, 0.933, 0.102, 1.0) # yellow

    ac.setText(self.data.banner, '')

    # Eww, only do this if you want to listen to more clicks dynamically.
    #if not hasattr(self.data, 'clicky')
    #  ac.addOnClickedListener(self.data.clicky, sys.modules['hot_app'].onClick)


  def acUpdate(self, delta_t):
    if sim_info.info.graphics.status != sim_info.AC_LIVE:
      # You probably do not want to do anything until the sim is active.
      return

    if self.first_update:
      # App was just hot reloaded, or is otherwise running for the first time.
      self.first_update = False
      self.reinitialize_app()

    new_text = (
      """
      Total Frames: {frame_count}
      Since Reload: {local_frame_count}
      TRY CHANGING THIS AND RUN 'client_debug.py send'
      Current Lap: {current_lap}
      Lap Time: {lap_time}
      """.format(frame_count = self.data.frame_count,
                 local_frame_count = self.local_frame_count,
                 current_lap = ac.getCarState(0, acsys.CS.LapCount),
                 lap_time = ac.getCarState(0, acsys.CS.LapTime)))

    ac.setText(self.data.banner, new_text)

  def onRender(self, delta_t):
    if self.first_update:
      return # bail out, nothing is ready

    # AC resets background opacity if the user moves the window.
    # Set it on every frame to force it.
    ac.setBackgroundOpacity(self.data.app_id, 0.0)

    # Our demo of frame count.
    self.local_frame_count += 1
    self.data.frame_count += 1

    # Example of hiding your label when in replay mode.
    if (sim_info.info.graphics.status not in (sim_info.AC_LIVE,
                                              sim_info.AC_PAUSE)):
      ac.setVisible(self.data.banner, 0)
    else:
      ac.setVisible(self.data.banner, 1)

  def onClick(self):
    if self.first_update:
      return # bail out, nothing is ready

    # Handle clicks here, see addOnClickedListener and ../hot_app.py addRender
    return


my_hot_app = HotApp()
