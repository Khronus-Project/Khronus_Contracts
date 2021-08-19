import pytest
from datetime import datetime, timezone
from brownie import accounts, TestKhronusNode
from testing_utils import logger, khron_constants_client

@pytest.fixture
def constants():
    return khron_constants_client()

@pytest.fixture
def current_utc_timestamp():
    return int(datetime.now(timezone.utc).timestamp())

def test_sendKhronRequest_happyPath(constants, current_utc_timestamp): 
    # Set up constants for testing
    token_contract = constants[0]
    coordinator_contract = constants[1]
    client_contract = constants[2]
    client_owner = constants[4]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    registration_deposit = 1*10**18
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    nodeContract_0 = TestKhronusNode.deploy({'from':node_owner_0})
    nodeContract_1 = TestKhronusNode.deploy({'from':node_owner_1})
    coordinator_contract.registerNode(nodeContract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(nodeContract_1.address,{'from':node_owner_1})
    # Set Test
    txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {'from':escrow_depositor})
    eventsOfInterest = txt.events['AlertDispatched'], txt.events['Transfer']
    #Test Log
    data = {'Test':'setKhronRequest_Two_Nodes','TestTime':datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime(), 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address, "Nodes":[nodeContract_0.address, nodeContract_1.address]}, "Events":eventsOfInterest}
    logger(data)
    # No Assertion
    assert (eventsOfInterest[0]["assignedNodes"][0] == nodeContract_0.address) and eventsOfInterest[0]["assignedNodes"][1] == nodeContract_1.address
    assert (eventsOfInterest[1][1]['to'] == nodeContract_0.address) and eventsOfInterest[1][2]['to'] == nodeContract_1.address

def test_sendKhronRequest_one_node_available(constants, current_utc_timestamp): 
    # Set up constants for testing
    token_contract = constants[0]
    coordinator_contract = constants[1]
    client_contract = constants[2]
    client_owner = constants[4]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    node_owner_0 = accounts[4]
    registration_deposit = 1*10**18
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    nodeContract_0 = TestKhronusNode.deploy({'from':node_owner_0})
    coordinator_contract.registerNode(nodeContract_0.address,{'from':node_owner_0})
    # Set Test
    txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {'from':escrow_depositor})
    eventOfInterest = txt.events['AlertDispatched']
    #Test Log
    data = {'Test':'setKhronRequest_One_Node','TestTime':datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime(), 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address, "Node":nodeContract_0.address}, "Events":eventOfInterest}
    logger(data)
    # No Assertion
    assert (eventOfInterest["assignedNodes"][0] == eventOfInterest["assignedNodes"][1]) and eventOfInterest["assignedNodes"][0] == nodeContract_0.address

def test_sendKhronRequest_no_nodes_available_error(constants, current_utc_timestamp): 
    # Set up constants for testing
    token_contract = constants[0]
    coordinator_contract = constants[1]
    client_contract = constants[2]
    client_owner = constants[4]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    registration_deposit = 1*10**18
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    # Set test
    isValid = True
    try:
        txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {'from':escrow_depositor})
        #Test Log
        data = {'Test':'setKhronRequest','TestTime':datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime(), 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address}, "Events":dict(txt.events)}
        logger(data)
        # No Assertion
    except Exception as e:
        data = {'Test':'setKhronRequest_Exception_no_nodes','TestTime':datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime(), 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address}, "Exception":e.message}
        logger(data)
        isValid = False
    assert coordinator_contract.nodeCorrelative() == 0
    assert not isValid

def test_multiple_call_credits_happy_path(constants, current_utc_timestamp):
    # Set up constants for testing
    token_contract = constants[0]
    coordinator_contract = constants[1]
    client_contract = constants[2]
    client_owner = constants[4]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    registration_deposit = 1*10**18
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    nodeContract_0 = TestKhronusNode.deploy({'from':node_owner_0})
    nodeContract_1 = TestKhronusNode.deploy({'from':node_owner_1})
    coordinator_contract.registerNode(nodeContract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(nodeContract_1.address,{'from':node_owner_1})
    isValid = True
    for i in range(10):
        txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent,{'from':escrow_depositor})
    assert i == 9

def test_multiple_call_credits_exception(constants, current_utc_timestamp):
    # Set up constants for testing
    token_contract = constants[0]
    coordinator_contract = constants[1]
    client_contract = constants[2]
    client_owner = constants[4]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    registration_deposit = 1*10**18
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    nodeContract_0 = TestKhronusNode.deploy({'from':node_owner_0})
    nodeContract_1 = TestKhronusNode.deploy({'from':node_owner_1})
    coordinator_contract.registerNode(nodeContract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(nodeContract_1.address,{'from':node_owner_1})
    result = ""
    try:
        for i in range(11):
            txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent,{'from':escrow_depositor})
    except Exception as e:
        result = e.message
    assert result == 'VM Exception while processing transaction: revert Not enough funds in contract to set request'