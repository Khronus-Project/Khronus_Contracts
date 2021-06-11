from brownie import KhronToken, TestKhronusClient, TestKhronusNode
from brownie import accounts
import json

def main(): 
    account = accounts.load('testing_account')
    KhronToken.deploy({'from':account})
    TestKhronusClient.deploy({'from':account})
    TestKhronusNode.deploy({'from':account})
    KhronToken[0].transfer(TestKhronusClient[0].address, 100000*10**18,{'from':account})
    TestKhronusClient[0].setKhronTokenAddress(KhronToken[0].address,{'from':account})
    contracts = {'KhronToken':KhronToken[0].address, 'TestKhronusClient':TestKhronusClient[0].address, 'TestKhronusNode':TestKhronusNode[0].address}
    with open ('../contract_library/contract_addresses_ext.json','w') as f:
        json.dump(contracts, f)