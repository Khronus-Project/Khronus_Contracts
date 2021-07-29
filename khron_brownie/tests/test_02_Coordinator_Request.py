import pytest
from datetime import datetime
from brownie import accounts, KhronusCoordinator, EscrowInfrastructure, KhronToken
from testing_utils import logger, khron_constants

@pytest.fixture
def constants():
    return khron_constants()

def test_sendKhronRequest(constants): 
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    clientContract = constants[2]
    clientOwner = constants[4]
    escrowDepositor = accounts[2]
    escrowBeneficiary = accounts[3]
    registrationDeposit = 1*10**18
    callPrice = 0.1*10**18
    timestamp = 1626521216
    # Set environment for testing
    tokenContract.increaseApproval(coordinatorContract.address, registrationDeposit, {'from':clientOwner})
    coordinatorContract.registerClient(clientContract.address, registrationDeposit, {'from':clientOwner})
    # Set test
    clientCommitedFunds = coordinatorContract.commitedFundsOf(clientContract.address)
    clientOwnerAllowance = tokenContract.allowance(coordinatorContract.address, clientOwner.address)
    escrowID = clientContract.openEscrow.call(escrowBeneficiary, timestamp, {'from':escrowDepositor})
    requestID = coordinatorContract.requestKhronTab.call(timestamp, 1, "",{'from':clientContract})
    txt = clientContract.openEscrow(escrowBeneficiary, timestamp, {'from':escrowDepositor})
    #Test Log
    data = {'Test':'setKhronRequest','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Client":clientContract.address}, "Events":dict(txt.events)}
    logger(data)
    # Assertion
    assert clientContract.retrieveEscrowID(requestID) == escrowID
    assert coordinatorContract.commitedFundsOf(clientContract.address) == clientCommitedFunds + callPrice
    assert tokenContract.allowance(coordinatorContract.address, clientOwner.address) == clientOwnerAllowance - callPrice