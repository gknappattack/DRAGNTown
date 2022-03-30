import requests
import json

class ServerCommunicator():
    ip = None
    port = None
    path = None
    def __init__(self, IP="localhost", PORT="8088", PATH="/"):
        self.ip = IP
        self.port = PORT
        self.path = PATH

    def set_ip(self, IP):
        self.ip = IP
    def set_port(self, PORT):
        self.port = PORT
    def set_path(self, PATH):
        self.path = PATH

    def send_recv_server(self, message):
        url = "http://" + self.ip + ":" + self.port + self.path
        json_message = {}
        json_message["text"] = message
        send_json = json.dumps(json_message)
        byte_res = requests.post(url, send_json)
        json_res = byte_res.text
        res = json.loads(json_res)
        print("RES: ", res)
        return res
        