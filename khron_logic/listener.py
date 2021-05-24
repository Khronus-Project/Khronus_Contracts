import os
from web3 import Web3
from dotenv import load_dotenv
import time
import json

load_dotenv()
node_provider = os.environ['NODE_PROVIDER']
web3_connection = Web3(Web3.HTTPProvider(node_provider))

with open('./khron_brownie/build/contracts/khron_logger.json') as f:
    abiJson = json.load(f)

contractAddress = '0x6A5d1eeFfD2D55Ac0B0B03e9f0502dF14A6eaD7C'
contract = web3_connection.eth.contract(address=contractAddress, abi=abiJson['abi'])
accounts = web3_connection.eth.accounts
transfer_Event = contract.events.Transfer() # Modification

def are_we_connected():
    return web3_connection.isConnected()

def handle_event(event):
    receipt = web3_connection.eth.waitForTransactionReceipt(event['transactionHash'])
    result = transfer_Event.processReceipt(receipt) # Modification
    print(result)

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)

block_filter = web3_connection.eth.filter({'fromBlock':'latest', 'address':contractAddress})
log_loop(block_filter, 2)
