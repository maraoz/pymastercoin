#! /usr/bin/python
"""Mastercoin main script""" 


import sys
import argparse
from bitcoinrpc import authproxy

from embed import recover_bytes_from_address
from message import MastercoinAddressMessage, CURR_ID_TESTCOIN, CURRENCIES, CURRENCY_NAME, DACOINMINISTERS_IN_MSC



def main(args):
    BITCOIN_RPC_URL = 'http://%s:%s@%s:%s/' % (args.username, args.password, args.host, args.port)
    
    bitcoin = authproxy.AuthServiceProxy(BITCOIN_RPC_URL)
    print args
    addresses = {}
    balances = {}
    results = bitcoin.listreceivedbyaddress()
    print "Your addresses, and balance (in BTC):"
    index = -1
    for result in results:
        index += 1
        addr, amount = result['address'], result['amount']
        balances[addr] = amount
        addresses[str(index)] = addr
        print "\t%s) %s\t%s BTC" % (index, addr, amount)
    
    
    if index == -1:
        print "You don't have any funds in any address. Please fund your Mastercoin address and retry."
        return
    
    print ""
    print "Select address to send from the list (%s-%s) and press ENTER. (default = 0)" % (0, index)
    selected_id = raw_input() or "0"
    sender = addresses.get(selected_id)
    if not sender:
        print "Error selecting address. Now exiting."
        return
    
    print "Please enter a recipient bitcoin address and press ENTER."
    recipient = raw_input() or "mkHz6UY7AjURz8wK4dYBzcGHaKmmSAPA3d"
    recover_bytes_from_address(recipient)  # checking if address is valid
    
    print "Which currency do you wish to send? (MasterCoin = 1, TestCoin = 2) (default = TestCoin)"
    currency_id = int(raw_input() or CURR_ID_TESTCOIN)
    if currency_id not in CURRENCIES:
        print "Error selecting currency. Now exiting."
        return
    
    print "How many %ss do you wish to send? (default = 1)" % (CURRENCY_NAME[currency_id])
    ammount = long(float(raw_input() or 1) * DACOINMINISTERS_IN_MSC)
    
    msc_msg = MastercoinAddressMessage.simple_send(sender, recipient, currency_id, ammount)
    
    data = msc_msg.broadcast(bitcoin)
    print "Mastercoin message broadcasted. Info:"
    print data

def parse():
    parser = argparse.ArgumentParser(description='PyMastercoin main script.')
    parser.add_argument('-u', '--username', type=str, nargs=1, required=True, help='the bitcoin-rpc username')
    parser.add_argument('-p', '--password', type=str, nargs=1, required=True, help='the bitcoin-rpc password')
    
    parser.add_argument('-H', '--host', type=str, nargs=1, default=["localhost"], help='the bitcoin-rpc host')
    parser.add_argument('-P', '--port', type=int, nargs=1, default=[8332], help='the bitcoin-rpc port')
    
    args = parser.parse_args()
    
    args.username = args.username[0]
    args.password = args.password[0]
    args.host = args.host[0]
    args.port = args.port[0]
    
    main(args)
    

if __name__ == '__main__':
    parse()
