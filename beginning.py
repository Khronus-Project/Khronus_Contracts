from web3 import Web3

node_provider = 'https://mainnet.infura.io/v3/87b50c7e7213473dbf790d4da8a899bf'

web3_connection = Web3(Web3.HTTPProvider(node_provider))

def are_we_connected():
    return web3_connection.isConnected()

def latest_block():
    return web3_connection.eth.get_block('latest').timestamp