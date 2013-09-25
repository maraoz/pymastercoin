"""Mastercoin message models""" 



from struct import pack
from embed import recover_bytes_from_address, embed_in_address, TESTNET

EXODUS_ADDRESS = "1EXoDusjGwvnjZUyKkxZ4UHEf77z6A5S4P" if not TESTNET else "mx4gSH1wfPdV7c9FNGxZLMGh1K4x43CVfT"


DACOINMINISTERS_IN_MSC = 100000000
EPSILON = float(0.00006)

CURR_ID_MASTERCOIN = 1
CURR_ID_TESTCOIN = 2

CURRENCIES = [None, CURR_ID_MASTERCOIN, CURR_ID_TESTCOIN]
CURRENCY_NAME = [None, "MasterCoin", "TestCoin"]

TX_TYPE_SIMPLESEND = 0

def build_data_simple_send(recipient, currency_id, ammount):
    recipient_seq = ord(recover_bytes_from_address(recipient)[1])
    data_seq = (recipient_seq - 1) % 256
    data_bytes = pack('!HIIQH', data_seq, TX_TYPE_SIMPLESEND, currency_id, ammount, 0)
    return data_bytes
    

class MastercoinMessage():
    """Generic Mastercoin Message."""
    
    @classmethod
    def simple_send(cls, sender, recipient, currency_id=CURR_ID_TESTCOIN, ammount=100000000):
        return cls(sender, recipient, build_data_simple_send(recipient, currency_id, ammount))
    
    def __init__(self, sender, reference, data):
        self.sender = sender
        self.reference = reference
        self.data = data
    
    
    def broadcast(self, bitcoin):
        """Subclasses should use the bitcoin-rpc client to broadcast the Mastercoin message"""
        raise NotImplementedError()
    
class MastercoinAddressMessage(MastercoinMessage):
    """Mastercoin message implementation using bitcoin address data encoding"""
        
    def broadcast(self, bitcoin):
        
        print "Broadcasting MasterCoin message. Raw data: %s" % self.data.encode("hex")
        
        data_address = embed_in_address(self.data)
        recover_bytes_from_address(data_address) # check validity
        
        txs = {
            EXODUS_ADDRESS:                 EPSILON,
            self.reference:                 EPSILON,
            data_address:                   EPSILON     # TODO: take into account data larger than 20 bytes
           }
        
        account = bitcoin.getaccount(self.sender)
        print "About to send the following transactions, are you sure?"
        print "\tExodus:\t\t%s -> %s" % (EXODUS_ADDRESS, EPSILON)
        print "\tReference:\t%s -> %s" % (self.reference, EPSILON)
        print "\tData:\t\t%s -> %s" % (data_address, EPSILON)
        print "Press ENTER to continue or anything else to cancel."
        if raw_input() == "":
            data = bitcoin.sendmany(account, txs)
            return data

class MastercoinMultisigMessage(MastercoinMessage):
    """Mastercoin message implementation using multisig data encoding"""
    
    def broadcast(self, bitcoin):
        pubkeys = [
            "0491bba2510912a5bd37da1fb5b1673010e43d2c6d812c514e91bfa9f2eb129e1c183329db55bd868e209aac2fbc02cb33d98fe74bf23f0c235d6126b1d8334f86",
            "04865c40293a680cb9c020e7b1e106d8c1916d3cef99aa431a56d253e69256dac09ef122b1a986818a7cb624532f062c1d1f8722084861c5c3291ccffef4ec6874",
            "048d2455d2403e08708fc1f556002f1b6cd83f992d085097f9974ab08a28838f07896fbab08f39495e15fa6fad6edbfb1e754e35fa1c7844c41f322a1863d46213"
        ]
        print bitcoin.createmultisig(2, )["address"]
        
