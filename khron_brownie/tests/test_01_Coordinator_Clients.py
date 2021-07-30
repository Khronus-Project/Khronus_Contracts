import pytest
from datetime import datetime
from testing_utils import logger, khron_constants_client

@pytest.fixture
def constants():
    return khron_constants_client()

def test_register_client(constants):
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    clientContract = constants[2]
    clientOwner = constants[4]
    registrationDeposit = 1*10**18
    # Test Body
    clientOwnerBalance = tokenContract.balanceOf(clientOwner.address)
    clientOwnerAllowance = tokenContract.allowance(coordinatorContract.address, clientOwner.address)
    coordinatorBalance = tokenContract.balanceOf(coordinatorContract.address)
    clientContractBalance = coordinatorContract.creditOf(clientContract.address)
    tokenContract.increaseApproval(coordinatorContract.address, registrationDeposit, {'from':clientOwner})
    txt = coordinatorContract.registerClient(clientContract.address, registrationDeposit, {'from':clientOwner})
    #Test Log
    data = {'Test':'registerClient','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Client":clientContract.address}, "Events":dict(txt.events)}
    logger(data)
    # Assertion
    assert tokenContract.balanceOf(clientOwner.address) == clientOwnerBalance - registrationDeposit
    assert tokenContract.balanceOf(coordinatorContract.address) == coordinatorBalance + registrationDeposit
    assert tokenContract.allowance(coordinatorContract.address, clientOwner.address) == clientOwnerAllowance + registrationDeposit
    assert coordinatorContract.creditOf(clientContract.address) == clientContractBalance + registrationDeposit

def test_fund_client(constants):
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    clientContract = constants[2]
    clientOwner = constants[4]
    registrationDeposit = 1*10**18
    clientCreditTokens = 50*10**18
    tokenContract.increaseApproval(coordinatorContract.address, registrationDeposit, {'from':clientOwner})
    coordinatorContract.registerClient(clientContract.address, registrationDeposit, {'from':clientOwner})
    # Test Body
    clientOwnerBalance = tokenContract.balanceOf(clientOwner.address)
    clientOwnerAllowance = tokenContract.allowance(coordinatorContract.address, clientOwner.address)
    coordinatorBalance = tokenContract.balanceOf(coordinatorContract.address)
    clientContractBalance = coordinatorContract.creditOf(clientContract.address)
    tokenContract.increaseApproval(coordinatorContract.address, clientCreditTokens, {'from':clientOwner})
    txt = coordinatorContract.fundClient(clientContract.address, clientCreditTokens, {'from':clientOwner})
    #Test Log
    data = {'Test':'fundClient','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Client":clientContract.address}, "Events":dict(txt.events)}
    logger(data)
    # Assertion
    assert tokenContract.balanceOf(clientOwner.address) == clientOwnerBalance - clientCreditTokens
    assert tokenContract.balanceOf(coordinatorContract.address) == coordinatorBalance + clientCreditTokens
    assert tokenContract.allowance(coordinatorContract.address, clientOwner.address) == clientOwnerAllowance + clientCreditTokens
    assert coordinatorContract.creditOf(clientContract.address) == clientContractBalance + clientCreditTokens