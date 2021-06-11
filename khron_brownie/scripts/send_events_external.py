from brownie import accounts, TestKhronusClient, TestKhronusNode
import json


def main():
    account = accounts.load('testing_account')
    with open ('../contract_library/contract_addresses_ext.json') as f:
        addresses = json.load(f)
    with open ('build/contracts/KhronusClient.json') as f:
        abiJson = json.load(f)
    tx = TestKhronusClient.at(addresses['TestKhronusClient']).setKhronTab(TestKhronusNode.at(addresses['TestKhronusNode']),10**18,'68656c6c6f20776f726c64',{'from':account})
    data = []
    for log in tx.logs:
        dir = {}
        dir['address'] = log.address
        dir['topics'] = log.topics
        data.append(dir)        
    print (data)