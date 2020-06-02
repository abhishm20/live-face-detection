import asyncio

import cv2
import numpy as np
import websockets


def extract_faces(img_str):
    jpg_as_np = np.frombuffer(img_str, dtype=np.uint8)
    gray = cv2.imdecode(jpg_as_np, flags=1)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=1,
        minSize=(30, 30)
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print("Found faces: ", len(faces))
    img_str = cv2.imencode('.jpg', gray)[1].tostring()
    return img_str


def server_program():
    async def handle_message(message):
        return extract_faces(message)
        pass

    async def consumer_handler(websocket, path):
        while True:
            message = await websocket.recv()
            await websocket.send(await handle_message(message))

    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # localhost_pem = pathlib.Path(__file__).with_name("cert.pem")
    # ssl_context.load_cert_chain(localhost_pem)
    #
    # start_server = websockets.serve(
    #     consumer_handler, "127.0.0.1", 9999, ssl=ssl_context
    # )

    start_server = websockets.serve(consumer_handler, '127.0.0.1', 9999)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    print("Starting")
    server_program()
