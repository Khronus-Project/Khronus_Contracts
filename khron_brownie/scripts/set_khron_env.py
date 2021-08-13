from brownie import accounts, TestKhronusNode
from scripts.scripts_utils import khron_constants_client
import json

def main():
    constants = khron_constants_client()
    # Set up constants 
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    clientContract = constants[2]
    clientOwner = constants[4]
    nodeOwner_0 = accounts[4]
    nodeOwner_1 = accounts[5]
    registrationDeposit = constants[5]
    # Set environment 
    tokenContract.increaseApproval(coordinatorContract.address, registrationDeposit, {'from':clientOwner})
    coordinatorContract.registerClient(clientContract.address, registrationDeposit, {'from':clientOwner})
    nodeContract_0 = TestKhronusNode.deploy({'from':nodeOwner_0})
    nodeContract_1 = TestKhronusNode.deploy({'from':nodeOwner_1})
    coordinatorContract.registerNode(nodeContract_0.address,{'from':nodeOwner_0})
    coordinatorContract.registerNode(nodeContract_1.address,{'from':nodeOwner_1})
    # Record environment
    contracts = {"KhronToken": tokenContract.address, "KhronusClient": clientContract.address, "KhronusCoordinator":coordinatorContract.address, "KhronusNode_0": nodeContract_0.address, "KhronusNode_1": nodeContract_1.address}
    with open ('../contract_library/contract_addresses.json','w') as f:
        json.dump(contracts, f)