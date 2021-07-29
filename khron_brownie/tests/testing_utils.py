
from brownie import accounts, KhronusCoordinator, EscrowInfrastructure, KhronToken
# Testing utilities

def khron_constants():
    # Constants
    totalClientTokens = 100*10**18
    registrationDeposit = 1*10**18
    callPrice = 0.1*10**18
    khronOwner = accounts[0]
    clientOwner = accounts[1]
    tokenContract = KhronToken.deploy({'from':khronOwner})
    coordinatorContract = KhronusCoordinator.deploy({'from':khronOwner})
    clientContract = EscrowInfrastructure.deploy(coordinatorContract.address,{'from':clientOwner})
    coordinatorContract.setKhronTokenAddress(tokenContract.address,{'from':khronOwner})
    tokenContract.transfer(clientOwner.address, totalClientTokens,{'from':khronOwner})
    coordinatorContract.setCallPrice(callPrice, {'from':khronOwner})
    coordinatorContract.setRegistrationDeposit(registrationDeposit, {'from':khronOwner})
    return (tokenContract, coordinatorContract, clientContract, khronOwner, clientOwner)

def logger(data):
    buffer = str(data)
    with open ('./tests/logger.txt', 'a') as f:
        f.write(buffer+'\n')