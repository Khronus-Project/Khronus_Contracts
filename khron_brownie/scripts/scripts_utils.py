from brownie import accounts, KhronusCoordinator, EscrowInfrastructure, KhronToken, TestKhronusNode
# Testing utilities

def khron_constants_client():
    # Constants
    totalClientTokens = 100*10**18
    registrationDeposit = 100*10**18
    callPrice = 0.01*10**18
    khronOwner = accounts[0]
    clientOwner = accounts[1]
    tokenContract = KhronToken.deploy({'from':khronOwner})
    coordinatorContract = KhronusCoordinator.deploy(tokenContract.address, registrationDeposit, callPrice,{'from':khronOwner})
    clientContract = EscrowInfrastructure.deploy(coordinatorContract.address,{'from':clientOwner})
    tokenContract.transfer(clientOwner.address, totalClientTokens,{'from':khronOwner})
    return (tokenContract, coordinatorContract, clientContract, khronOwner, clientOwner, registrationDeposit, callPrice)
    