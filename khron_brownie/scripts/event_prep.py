from brownie import accounts, KhronToken, TestKhronusCoordinator, TestKhronusNode, InterestDeposit
import json

def main():
    KhronToken.deploy({'from':accounts[0]})
    TestKhronusCoordinator.deploy({'from':accounts[0]})
    TestKhronusNode.deploy({'from':accounts[0]})
    InterestDeposit.deploy({'from':accounts[0]})
    KhronToken[0].transfer(TestKhronusCoordinator[0].address, 100000*10**18,{'from':accounts[0]})
    TestKhronusCoordinator[0].setKhronTokenAddress(KhronToken[0].address)
    InterestDeposit[0].openAccount(accounts[1].address, 100)
    contracts = {'KhronToken':KhronToken[0].address, 'TestKhronusCoordinator':TestKhronusCoordinator[0].address, 'TestKhronusNode':TestKhronusNode[0].address, 'InterestDeposit':InterestDeposit[0].address}
    with open ('../contract_library/contract_addresses.json','w') as f:
        json.dump(contracts, f)