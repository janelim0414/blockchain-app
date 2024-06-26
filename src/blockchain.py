from block import Block

class Blockchain:
    def __init__(self, chain=None, block_number=None, most_recent_hash=None, hash_requirement=None):
        """
        initialize a blockchain
        
        parameters:
        chain - list of Block types
        block_number - int
        most_recent_hash - str
        hash_requirement - str
        """
        if hash_requirement:
            self.hash_requirement = hash_requirement
        else:
            self.hash_requirement = '0000'  # a hash is valid only if the first four characters exactly match the hash_difficulty

        if chain:
            self.chain = chain
        else:
            self.chain = [self.create_genesis_block()]
        if block_number:
            self.block_number = block_number
        else:
            self.block_number = 1
        if most_recent_hash:
            self.most_recent_hash = most_recent_hash
        else:
            self.most_recent_hash = self.get_last_block().curr_hash

    def create_genesis_block(self):
        """
        create a dummy head for the block chain
        """
        genesis_block = Block(1, 'Genesis', '0')
        genesis_block.mine(self.hash_requirement)
        self.most_recent_hash = genesis_block.curr_hash
        return genesis_block
    
    def valid_proof(self, new_block, new_block_hash):
        """
        validate that the new block's prev_hash is valid
        
        arguments:
        new_block - Block data to be added to chain (Block)
        new_block_hash - Hash of the new block data (str)

        returns: valid hash (bool)
        """
        return new_block_hash.startswith(self.hash_requirement) and new_block_hash == new_block.get_hash(new_block.nonce)
    
    def add_block(self, new_block, new_block_hash):
        """
        validate that the new block's prev_hash is valid and if so, create a new Block object and add it to the chain
        
        arguments:
        new_block: Block data to be added to chain (Block)
        new_block_hash: Hash of the new block data (str)

        returns: most recent hash (str)
        """
        if new_block.prev_hash == self.most_recent_hash and self.valid_proof(new_block, new_block_hash):
            self.block_number += 1
            self.chain.append(new_block)
            self.most_recent_hash = new_block.curr_hash
            return self.most_recent_hash
        else:
            raise Exception('Invalid prev_hash')

    def get_chain(self):
        """
        return the whole chain        
        """
        return self.chain
    
    def get_last_block(self):
        """
        return the last block in the chain       
        """
        return self.chain[-1]
    
    def print_chain(self):
        """
        a debugging function that print the whole chain
        """
        return '\n'.join(str(block) for block in self.get_chain())
