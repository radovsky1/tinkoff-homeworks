from flask import Flask, jsonify, request

from ..service import BlockchainInterface


class Handler:

    def __init__(self, service: BlockchainInterface):
        self.service = service

    def init_routes(self, app: Flask):
        app.route("/mine_block", methods=["GET"])(self.mine_block)
        app.route("/valid", methods=["GET"])(self.valid)
        app.route("/get_chain", methods=["GET"])(self.get_chain)
        app.route("/block/<int:block_id>/status", methods=["GET"])(self.get_block_status)

    def mine_block(self):
        previous_block = self.service.get_previous_block()
        previous_proof = previous_block.proof

        proof = self.service.proof_of_work(previous_proof)
        previous_hash = self.service.make_hash(previous_block)

        block = self.service.create_block(proof, previous_hash)

        response = {
            "message": "Block created",
            "index": block.index,
            "timestamp": block.timestamp,
            "proof": block.proof,
            "previous_hash": block.previous_hash,
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
