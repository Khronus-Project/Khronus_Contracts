import pytest, json, pathlib
from datetime import datetime
from brownie import accounts, KhronusCoordinator, EscrowInfrastructure, KhronToken

@pytest.fixture
def constants():
    # Constants
    khronOwner = accounts[0]
    clientOwner = accounts[1]
    tokenContract = KhronToken.deploy({'from':khronOwner})
    coordinatorContract = KhronusCoordinator.deploy({'from':khronOwner})
    clientContract = EscrowInfrastructure.deploy(coordinatorContract.address,{'from':clientOwner})
    return (tokenContract, coordinatorContract, clientContract, khronOwner, clientOwner)

def test_fundClient(constants):
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    clientContract = constants[2]
    khronOwner = constants[3]
    clientOwner = constants[4]
    totalClientTokens = 100*10**18
    clientCreditTokens = 50*10**18
    coordinatorContract.setKhronTokenAddress(tokenContract.address,{'from':khronOwner})
    # Test Body
    clientOwnerBalance = tokenContract.balanceOf(clientOwner.address)
    clientOwnerAllowance = tokenContract.allowance(coordinatorContract.address, clientOwner.address)
    coordinatorBalance = tokenContract.balanceOf(coordinatorContract.address)
    clientContractBalance = coordinatorContract.creditOf(clientContract.address)
    tokenContract.transfer(clientOwner.address, totalClientTokens,{'from':khronOwner})
    tokenContract.increaseApproval(coordinatorContract.address, clientCreditTokens, {'from':clientOwner})
    txt = coordinatorContract.fundClient(clientContract.address, clientCreditTokens, {'from':clientOwner})
    #Test Log
    data = {'Test':'fundClient','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Client":clientContract.address}, "Events":dict(txt.events)}
    log_data(data)
    # Assertion
    assert tokenContract.balanceOf(clientOwner.address) == clientOwnerBalance + clientCreditTokens
    assert tokenContract.balanceOf(coordinatorContract.address) == coordinatorBalance + clientCreditTokens
    assert tokenContract.allowance(coordinatorContract.address, clientOwner.address) == clientOwnerAllowance + clientCreditTokens
    assert coordinatorContract.creditOf(clientContract.address) == clientContractBalance + clientCreditTokens

def test_sendKhronRequest(constants): 
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    clientContract = constants[2]
    khronOwner = constants[3]
    clientOwner = constants[4]
    escrowDepositor = accounts[2]
    escrowBeneficiary = accounts[3]
    totalClientTokens = 100*10**18
    clientCreditTokens = 50*10**18
    callPrice = 0.1*10**18
    timestamp = 1626521216
    # Set environment for testing
    coordinatorContract.setKhronTokenAddress(tokenContract.address,{'from':khronOwner})
    tokenContract.transfer(clientOwner.address, totalClientTokens,{'from':khronOwner})
    tokenContract.increaseApproval(coordinatorContract.address, clientCreditTokens, {'from':clientOwner})
    coordinatorContract.fundClient(clientContract.address, clientCreditTokens, {'from':clientOwner})
    coordinatorContract.setCallPrice(callPrice, {'from':khronOwner})
    clientCommitedFunds = coordinatorContract.commitedFundsOf(clientContract.address)
    clientOwnerAllowance = tokenContract.allowance(coordinatorContract.address, clientOwner.address)
    # Set test
    escrowID = clientContract.openEscrow.call(escrowBeneficiary, timestamp, {'from':escrowDepositor})
    requestID = coordinatorContract.requestKhronTab.call(timestamp, 1, "",{'from':clientContract})
    txt = clientContract.openEscrow(escrowBeneficiary, timestamp, {'from':escrowDepositor})
    #Test Log
    data = {'Test':'setKhronRequest','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Client":clientContract.address}, "Events":dict(txt.events)}
    log_data(data)
    # Assertion
    assert clientContract.retrieveEscrowID(requestID) == escrowID
    assert coordinatorContract.commitedFundsOf(clientContract.address) == clientCommitedFunds + callPrice
    assert tokenContract.allowance(coordinatorContract.address, clientOwner.address) == clientOwnerAllowance - callPrice


# Testing utilities
def log_data(data):
    buffer = str(data)
    with open ('./tests/logger.txt', 'a') as f:
        f.write(buffer+'\n')