from brownie import accounts, KhronToken, TestKhronusClient, TestKhronusNode
import json

def main():
    KhronToken.deploy({'from':accounts[0]})
    TestKhronusClient.deploy({'from':accounts[0]})
    TestKhronusNode.deploy({'from':accounts[0]})
    KhronToken[0].transfer(TestKhronusClient[0].address, 100000*10**18,{'from':accounts[0]})
    TestKhronusClient[0].setKhronTokenAddress(KhronToken[0].address)
    contracts = {'KhronToken':KhronToken[0].address, 'TestKhronusClient':TestKhronusClient[0].address, 'TestKhronusNode':TestKhronusNode[0].address}
    with open ('../contract_library/contract_addresses.json','w') as f:
        json.dump(contracts, f)