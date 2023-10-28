from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)

server_limit = 9

somefrek = [
  ["4189cf8e-a925-4a73-9051-88b4798ec5df", "s5MZ8h57Od6mhQbs0sstuyRMGumQrMEB4FaMNnZY", 0],
  ["08e39cd1-e942-4682-81e1-46ecb124c5a7", "sbblyyEImYDaCayJ1G9BkbscgYx4KlhKwdVn4s9T", 0],
  ["61bca84c-f3e6-447b-b71c-29d2abe30f7e", "sWUT9x2UAynDZU9nNyArDV3hljctMj461iPEw5iq", 0],
  ["eb73e10f-1a68-4979-9e30-a564dda495ac", "sn27OeHSuySQPnQyiNw9h5eFewEm8hSQwjqiaQRf", 0],
  ["d84506c8-4756-4d67-ab3a-8b1ec53121a6", "szSjtVFYQTiafmxg4RKhKMct32AWD7dnWKGQZFmb", 0]
]

timeouts = []

@app.route('/')
def home():
    return '', 401

@app.route('/status')
def status():
    return jsonify(somefrek)

@app.route('/get')
def get():
    somefrek.sort(key=lambda x: x[1])
    for server in somefrek:
        if server[1] < server_limit:
            server[1] += 1
            print("using server : " + server[0] + " with the usage of " + str(server[1]))
            timeouts.append({
                "id": server[0],
                "timeout": time.time() + 60
            })
            return jsonify(server)
    return '', 404

@app.route('/done/<id>', methods=['POST'])
def done(id):
    for server in somefrek:
        if server[0] == id:
            for t in timeouts:
                if t['id'] == server[0] and time.time() < t['timeout']:
                    timeouts.remove(t)
                    break
            server[1] -= 1
            if server[1] < 0: server[1] = 0
            print("releasing server : " + server[0] + " with the usage of " + str(server[1]))
            return jsonify(server)
    return '', 404

if __name__ == '__main__':
    app.run(port=3000)
