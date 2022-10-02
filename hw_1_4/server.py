from flask import Flask, jsonify, request

from hw_1_4.app.service import Blockchain
from hw_1_4.app.handlers import Handler

if __name__ == "__main__":
    app = Flask(__name__)
    blockchain = Blockchain()
    handler = Handler(blockchain)
    handler.init_routes(app)
    app.run(host="127.0.0.1", debug=True, port=5000)