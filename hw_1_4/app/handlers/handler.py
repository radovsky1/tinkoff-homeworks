import threading

from flask import Flask, jsonify, request

from ..service import BlockchainInterface


class APIConstants(object):
    """
    Blockchain API endpoints
    """
    MINE_BLOCK_ENDPOINT = "/mine_block"
    GET_CHAIN_ENDPOINT = "/get_chain"
    VALID_ENDPOINT = "/valid"
    GET_BLOCK_STATUS_ENDPOINT = "/block/<int:block_id>/status"


class Handler:

    def __init__(self, service: BlockchainInterface):
        self.service = service

    def init_routes(self, app: Flask):
        app.route(APIConstants.MINE_BLOCK_ENDPOINT, methods=["GET"])(
            self.mine_block
        )
        app.route(APIConstants.VALID_ENDPOINT, methods=["GET"])(
            self.valid
        )
        app.route(APIConstants.GET_CHAIN_ENDPOINT, methods=["GET"])(
            self.get_chain
        )
        app.route(APIConstants.GET_BLOCK_STATUS_ENDPOINT, methods=["GET"])(
            self.get_block_status
        )

    def mine_block(self):
        new_block_id = self.service.get_next_block_index()

        t = threading.Thread(target=self.service.mine_block)
        t.start()

        response = {
            "message": "Mining in progress",
            "block_index": new_block_id,
        }

        return jsonify(response), 200

    def valid(self):
        return jsonify({
            "chain_valid": "OK" if self.service.is_chain_valid() else "NOT OK"
        }), 200

    def get_chain(self):
        chain = [block.toDict() for block in self.service.get_chain()]

        return jsonify({
            "chain": chain
        }), 200

    def get_block_status(self, block_id: int):
        return jsonify({
            "block_status": self.service.get_block_status(block_id).value
        }), 200
