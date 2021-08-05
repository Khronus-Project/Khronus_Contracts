import pytest
from datetime import datetime
from brownie import accounts, TestKhronusNode
from testing_utils import logger, khron_constants_client

@pytest.fixture
def constants():
    return khron_constants_client()

def test_sendKhronRequest_happyPath(constants): 
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    clientContract = constants[2]
    clientOwner = constants[4]
    escrowDepositor = accounts[2]
    escrowBeneficiary = accounts[3]
    nodeOwner_0 = accounts[4]
    nodeOwner_1 = accounts[5]
    registrationDeposit = 1*10**18
    timestamp = 1626521216
    # Set environment for testing
    tokenContract.increaseApproval(coordinatorContract.address, registrationDeposit, {'from':clientOwner})
    coordinatorContract.registerClient(clientContract.address, registrationDeposit, {'from':clientOwner})
    nodeContract_0 = TestKhronusNode.deploy({'from':nodeOwner_0})
    nodeContract_1 = TestKhronusNode.deploy({'from':nodeOwner_1})
    coordinatorContract.registerNode(nodeContract_0.address,{'from':nodeOwner_0})
    coordinatorContract.registerNode(nodeContract_1.address,{'from':nodeOwner_1})
    # Set Test
    txt = clientContract.openEscrow(escrowBeneficiary, timestamp, {'from':escrowDepositor})
    eventsOfInterest = txt.events['AlertDispatched'], txt.events['Transfer']
    #Test Log
    data = {'Test':'setKhronRequest_Two_Nodes','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Client":clientContract.address, "Nodes":[nodeContract_0.address, nodeContract_1.address]}, "Events":eventsOfInterest}
    logger(data)
    # No Assertion
    assert (eventsOfInterest[0]["assignedNodes"][0] == nodeContract_0.address) and eventsOfInterest[0]["assignedNodes"][1] == nodeContract_1.address
    assert (eventsOfInterest[1][1]['to'] == nodeContract_0.address) and eventsOfInterest[1][2]['to'] == nodeContract_1.address

def test_sendKhronRequest_one_node_available(constants): 
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    clientContract = constants[2]
    clientOwner = constants[4]
    escrowDepositor = accounts[2]
    escrowBeneficiary = accounts[3]
    nodeOwner_0 = accounts[4]
    registrationDeposit = 1*10**18
    timestamp = 1626521216
    # Set environment for testing
    tokenContract.increaseApproval(coordinatorContract.address, registrationDeposit, {'from':clientOwner})
    coordinatorContract.registerClient(clientContract.address, registrationDeposit, {'from':clientOwner})
    nodeContract_0 = TestKhronusNode.deploy({'from':nodeOwner_0})
    coordinatorContract.registerNode(nodeContract_0.address,{'from':nodeOwner_0})
    # Set Test
    txt = clientContract.openEscrow(escrowBeneficiary, timestamp, {'from':escrowDepositor})
    eventOfInterest = txt.events['AlertDispatched']
    #Test Log
    data = {'Test':'setKhronRequest_One_Node','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Client":clientContract.address, "Node":nodeContract_0.address}, "Events":eventOfInterest}
    logger(data)
    # No Assertion
    assert (eventOfInterest["assignedNodes"][0] == eventOfInterest["assignedNodes"][1]) and eventOfInterest["assignedNodes"][0] == nodeContract_0.address

def test_sendKhronRequest_no_nodes_available_error(constants): 
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    clientContract = constants[2]
    clientOwner = constants[4]
    escrowDepositor = accounts[2]
    escrowBeneficiary = accounts[3]
    registrationDeposit = 1*10**18
    timestamp = 1626521216
    # Set environment for testing
    tokenContract.increaseApproval(coordinatorContract.address, registrationDeposit, {'from':clientOwner})
    coordinatorContract.registerClient(clientContract.address, registrationDeposit, {'from':clientOwner})
    # Set test
    isValid = True
    try:
        txt = clientContract.openEscrow(escrowBeneficiary, timestamp, {'from':escrowDepositor})
        #Test Log
        data = {'Test':'setKhronRequest','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Client":clientContract.address}, "Events":dict(txt.events)}
        logger(data)
        # No Assertion
    except Exception as e:
        data = {'Test':'setKhronRequest_Exception','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Client":clientContract.address}, "Exception":e.message}
        logger(data)
        isValid = False
    assert coordinatorContract.nodeCorrelative() == 0
    assert not isValid

def test_multiple_call_credits_happy_path(constants):
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    clientContract = constants[2]
    clientOwner = constants[4]
    escrowDepositor = accounts[2]
    escrowBeneficiary = accounts[3]
    nodeOwner_0 = accounts[4]
    nodeOwner_1 = accounts[5]
    registrationDeposit = 1*10**18
    timestamp = 1626521216
    # Set environment for testing
    tokenContract.increaseApproval(coordinatorContract.address, registrationDeposit, {'from':clientOwner})
    coordinatorContract.registerClient(clientContract.address, registrationDeposit, {'from':clientOwner})
    nodeContract_0 = TestKhronusNode.deploy({'from':nodeOwner_0})
    nodeContract_1 = TestKhronusNode.deploy({'from':nodeOwner_1})
    coordinatorContract.registerNode(nodeContract_0.address,{'from':nodeOwner_0})
    coordinatorContract.registerNode(nodeContract_1.address,{'from':nodeOwner_1})
    isValid = True
    for i in range(10):
        txt = clientContract.openEscrow(escrowBeneficiary, timestamp, {'from':escrowDepositor})
    assert i == 9

def test_multiple_call_credits_exception(constants):
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    clientContract = constants[2]
    clientOwner = constants[4]
    escrowDepositor = accounts[2]
    escrowBeneficiary = accounts[3]
    nodeOwner_0 = accounts[4]
    nodeOwner_1 = accounts[5]
    registrationDeposit = 1*10**18
    timestamp = 1626521216
    # Set environment for testing
    tokenContract.increaseApproval(coordinatorContract.address, registrationDeposit, {'from':clientOwner})
    coordinatorContract.registerClient(clientContract.address, registrationDeposit, {'from':clientOwner})
    nodeContract_0 = TestKhronusNode.deploy({'from':nodeOwner_0})
    nodeContract_1 = TestKhronusNode.deploy({'from':nodeOwner_1})
    coordinatorContract.registerNode(nodeContract_0.address,{'from':nodeOwner_0})
    coordinatorContract.registerNode(nodeContract_1.address,{'from':nodeOwner_1})
    result = ""
    try:
        for i in range(11):
            txt = clientContract.openEscrow(escrowBeneficiary, timestamp, {'from':escrowDepositor})
    except Exception as e:
        result = e.message
    assert result == 'VM Exception while processing transaction: revert Not enough funds in contract to set request'