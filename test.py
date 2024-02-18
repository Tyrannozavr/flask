import requests
from threading import Thread

response = ''
def send_request():
    global response
    response = requests.get('http://127.0.0.1:5000/update?city=Moscow&userId=2')


thread_pool = [
    Thread(target=send_request, args=[]) for _ in range(1000)
]

for thread in thread_pool:
    thread.start()
print(response.json())