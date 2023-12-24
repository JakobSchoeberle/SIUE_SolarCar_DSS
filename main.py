import threading
import WebSockets as Web
VideoEnable = False

Value1 = 140
Value2 = 180

if (VideoEnable == True):
    Videothread = threading.Thread(target=Web.Video_Server)
    Videothread.start()

Datathread = threading.Thread(target=Web.Data_Server)
Datathread.start()

# ---- Input ----
