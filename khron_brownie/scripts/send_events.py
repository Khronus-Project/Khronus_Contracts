from brownie import accounts, TestKhronusClient, TestKhronusNode
import eth_event
import json

#Hex 'hello world' 68656c6c6f20776f726c64
#Hex 'this is real' 74686973206973207265616c

def main():
    with open ('../contract_library/contract_addresses.json') as f:
        addresses = json.load(f)
    with open ('build/contracts/KhronusClient.json') as f:
        abiJson = json.load(f)
    tx = TestKhronusClient.at(addresses['TestKhronusClient']).setKhronTab(TestKhronusNode.at(addresses['TestKhronusNode']),10**18,'74686973206973207265616c',{'from':accounts[0]})
    data = []
    for log in tx.logs:
        dir = {}
        dir['address'] = log.address
        dir['topics'] = log.topics
        data.append(dir)        
    print (data)