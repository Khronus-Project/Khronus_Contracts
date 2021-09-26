from brownie import accounts, KhronusCoordinator, EscrowInfrastructure, KhronToken, TestKhronusNode
import json
# Testing utilities

def khron_constants_client():
    # Constants
    protocolOwner = accounts.load("KhronTestMaster")
    clientOwner = accounts.load("KhronTestClient")
    totalClientTokens = 100*10**18
    registrationDeposit = 100*10**18
    callPrice = 0.01*10**18
    khronOwner = protocolOwner
    tokenContract = KhronToken.deploy({'from':khronOwner})
    coordinatorContract = KhronusCoordinator.deploy(tokenContract.address, registrationDeposit, callPrice,{'from':khronOwner})
    clientContract = EscrowInfrastructure.deploy(coordinatorContract.address,{'from':clientOwner})
    tokenContract.transfer(clientOwner.address, totalClientTokens,{'from':khronOwner})
    return (tokenContract, coordinatorContract, clientContract, khronOwner, clientOwner, registrationDeposit, callPrice)

def main():
    constants = khron_constants_client()
    # Set up constants 
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    clientContract = constants[2]
    clientOwner = constants[4]
    nodeOwner_0 = accounts.load("KhronTestNode")
    registrationDeposit = constants[5]
    # Set environment 
    tokenContract.increaseApproval(coordinatorContract.address, registrationDeposit, {'from':clientOwner})
    coordinatorContract.registerClient(clientContract.address, registrationDeposit, {'from':clientOwner})
    nodeContract_0 = TestKhronusNode.deploy(coordinatorContract.address,{'from':nodeOwner_0})
    coordinatorContract.registerNode(nodeContract_0.address,{'from':nodeOwner_0})
    # Record environment
    contracts = {"KhronToken": tokenContract.address, "KhronusClient": clientContract.address, "KhronusCoordinator":coordinatorContract.address, "KhronusNode_0": nodeContract_0.address}
    with open ('../contract_library/contract_addresses_deployment.json','w') as f:
        json.dump(contracts, f)