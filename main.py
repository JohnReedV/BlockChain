from hashlib import sha256

def hashuptodate(*args):
    hashing_text = ""; h = sha256()

    for arg in args:
        hashing_text += str(arg)

    h.update(hashing_text.encode('utf-8'))
    return h.hexdigest()

class Block():

    def __init__(self, number = 0, previous_hash= "0" * 64, data = None, nonce = 0):
        self.data = data
        self.number = number
        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash(self):
        return hashuptodate(
            self.number,
            self.previous_hash,
            self.data,
            self.nonce
        )

    def __str__(self):
        return str("Block#: %s\nHash: %s\nPrevious: %s\nData: %s\nNonce: %s\n" %(
            self.number,
            self.hash(),
            self.previous_hash,
            self.data,
            self.nonce
            )
        )

class Blockchain():
    difficulty = 4

    def __init__(self):
        self.chain = []

    def add(self, block):
        self.chain.append(block)

    def remove(self, block):
        self.chain.remove(block)

    def mine(self, block):
        try: block.previous_hash = self.chain[-1].hash()
        except IndexError: pass

        while True:
            if block.hash()[:self.difficulty] == "0" * self.difficulty:
                self.add(block); break
            else:
                block.nonce += 1

    def isValid(self):
        for i in range(1, len(self.chain)):
            previous = self.chain[i].previous_hash
            current = self.chain[i-1].hash()
            if previous != current or current[:self.difficulty] != "0" * self.difficulty:
                return False

        return True

def main():
    blockchain = Blockchain()
    # these inputs are data in place of transactions
    t1 = input("give me data 1/4: ")
    t2 = input("give me data 2/4: ")
    t3 = input("give me data 3/4: ")
    t4 = input("give me data 4/4: ")
    database = [t1, t2, t3, t4]

    num = 0
    for data in database:
        num += 1
        blockchain.mine(Block(num, data=data))

    for block in blockchain.chain:
        print(block)

    print(f"Not corrupt: {blockchain.isValid()}")



main()