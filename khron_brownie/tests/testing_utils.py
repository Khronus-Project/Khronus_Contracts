
from brownie import accounts, KhronusCoordinator, EscrowInfrastructure, KhronToken, TestKhronusNode
# Testing utilities

def khron_constants_client():
    # Constants
    totalClientTokens = 100*10**18
    registrationDeposit = 1*10**18
    callPrice = 0.1*10**18
    khronOwner = accounts[0]
    clientOwner = accounts[1]
    tokenContract = KhronToken.deploy({'from':khronOwner})
    coordinatorContract = KhronusCoordinator.deploy(tokenContract.address, registrationDeposit, callPrice,{'from':khronOwner})
    clientContract = EscrowInfrastructure.deploy(coordinatorContract.address,{'from':clientOwner})
    tokenContract.transfer(clientOwner.address, totalClientTokens,{'from':khronOwner})
    return (tokenContract, coordinatorContract, clientContract, khronOwner, clientOwner)

def khron_constants_node():
    registrationDeposit = 1*10**18
    callPrice = 0.1*10**18
    khronOwner = accounts[0]
    nodeOwner_0 = accounts[4]
    tokenContract = KhronToken.deploy({'from':khronOwner})
    coordinatorContract = KhronusCoordinator.deploy(tokenContract.address, registrationDeposit, callPrice,{'from':khronOwner})
    nodeContract_0 = TestKhronusNode.deploy({'from':nodeOwner_0})
    return (tokenContract, coordinatorContract, nodeContract_0, khronOwner, nodeOwner_0)

def logger(data):
    buffer = str(data)
    with open ('./tests/logger.txt', 'a') as f:
        f.write(buffer+'\n')