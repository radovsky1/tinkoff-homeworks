import abc


class BlockchainInterface(metaclass=abc.ABCMeta):
    """
    Interface for blockchain service
    """

    @abc.abstractmethod
    def create_block(self, proof, previous_hash):
        pass

    @abc.abstractmethod
    def get_previous_block(self):
        pass

    @abc.abstractmethod
    def make_hash(self, block):
        pass

    @abc.abstractmethod
    def get_chain(self):
        pass

    @abc.abstractmethod
    def is_chain_valid(self):
        pass

    @abc.abstractmethod
    def get_block_status(self, block_id):
        pass

    @abc.abstractmethod
    def proof_of_work(self, previous_proof):
        pass
