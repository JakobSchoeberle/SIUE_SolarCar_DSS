import threading
import WebSockets as Web
VideoEnable = False

if (VideoEnable == True):
    Videothread = threading.Thread(target=Web.Video_Server)
    Videothread.start()

Datathread = threading.Thread(target=Web.Data_Server)
Datathread.start()

# ---- Input ----
