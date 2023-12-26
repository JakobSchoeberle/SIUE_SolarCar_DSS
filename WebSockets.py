import cv2
import asyncio
import websockets
import Common as Global

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
        await websocket.send("Value1 " + str(Global.Values[0]))
        await websocket.send("Value2 " + str(Global.Values[1]))
        await websocket.send("Value3 " + str(Global.Values[2]))
        await websocket.send("Value4 " + str(Global.Values[3]))
        await websocket.send("Value5 " + str(Global.Values[4]))
        await websocket.send("Value6 " + str(Global.Values[5]))
        await websocket.send("Value7 " + str(Global.Values[6]))
        await websocket.send("Value8 " + str(Global.Values[7]))
        await websocket.send("Value9 " + str(Global.Values[8]))
        await websocket.send("Value10 " + str(Global.Values[9]))
     
def Video_Server():
    videoloop = asyncio.new_event_loop()
    asyncio.set_event_loop(videoloop)

    start_video_server = websockets.serve(Video, "192.168.86.249", 9997)  
    videoloop.run_until_complete(start_video_server)
    videoloop.run_forever()
    #videoloop.close()

def Data_Server():
    dataloop = asyncio.new_event_loop()
    asyncio.set_event_loop(dataloop)

    start_Data_server = websockets.serve(Data, "192.168.86.249", 9998)    
    dataloop.run_until_complete(start_Data_server)
    dataloop.run_forever()
    dataloop.close()

