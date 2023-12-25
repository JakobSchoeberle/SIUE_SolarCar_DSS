import threading
import WebSockets as Web
import Common as Global
VideoEnable = False

if (VideoEnable == True):
    Videothread = threading.Thread(target=Web.Video_Server)
    Videothread.start()

Datathread = threading.Thread(target=Web.Data_Server)
Datathread.start()

# ---- Input ----s

Value1 = 140
Global.Values[0] = Value1
Value2 = 180
Global.Values[1] = Value2
