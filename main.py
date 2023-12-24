
import asyncio
import websockets
import threading
import cv2
    
async def Video(websocket, path):

    while True:

        camera = True
        if camera == True:

            vid = cv2.VideoCapture(0)
        else:
            vid = cv2.VideoCapture('videos/video1.mp4')
        try:
            while(vid.isOpened()):
                img, frame = vid.read()
                
                frame = cv2.resize(frame, (640, 480))
                encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 65]
                man = cv2.imencode('.jpg', frame, encode_param)[1]
                #sender(man)
                await websocket.send(man.tobytes())
                await websocket.wait_closed()
        except:
            pass

async def Data(websocket, path):
    while True:
        Value1 = 1
        await websocket.send(str(Value1))
        Value2 = 2
        await websocket.send(str(Value2))
     
def Video_Server():
    videoloop = asyncio.new_event_loop()
    asyncio.set_event_loop(videoloop)

    start_video_server = websockets.serve(Video, "127.0.0.1", 9997)  
    videoloop.run_until_complete(start_video_server)
    videoloop.run_forever()
    videoloop.close()

def Data_Server():
    dataloop = asyncio.new_event_loop()
    asyncio.set_event_loop(dataloop)

    start_Data_server = websockets.serve(Data, "127.0.0.1", 9998)    
    dataloop.run_until_complete(start_Data_server)
    dataloop.run_forever()
    dataloop.close()

Videothread = threading.Thread(target=Video_Server)
Videothread.start()

Datathread = threading.Thread(target=Data_Server)
Datathread.start()

print("things")

#asyncio.get_event_loop().run_forever()
