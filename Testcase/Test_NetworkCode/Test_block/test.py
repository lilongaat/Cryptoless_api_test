from time import sleep
import socketio

# 测试环境订阅
url = "http://52.77.230.103:4001/"
auth = {
    "token":"eyJzaWduYXR1cmUiOiIweDdjZDc5ODEzNjViNjU4M2Q1YjRiZjRhMjIxNjc4NzdmMzYwYjcxOWQ3ZjExNTk2OGUyYjEzOGIwMTM0ODcxNDA0N2M3NWQxNmQ3NTgxYmRhNjczNGZjYTk2MTVhMTE1OTcyY2QwMWFhY2E4MGYwZjczMTI0MWIzNWJmMDZkNTUzMWMiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogNzEzNjQ5NDFcbklzc3VlZCBBdDogVGh1LCAxNyBOb3YgMjAyMiAxNDozOToxNSBHTVRcbkV4cGlyYXRpb24gVGltZTogTW9uLCAxNyBOb3YgMjA0MiAxNDozOToxNSBHTVQifQ=="
}

sio = socketio.Client()
sio.connect(url=url,auth=auth)

while True:
    subscribe = {"id":"c99bc1e1-3dd5-41b4-851a-92951250bcbd","scope":["instructions"]}
    data = sio.emit(subscribe)
    sleep(1)
    print((data))