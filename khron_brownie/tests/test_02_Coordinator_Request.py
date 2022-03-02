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
    token_contract = constants["Token_Contract"]
    coordinator_contract = constants["Coordinator_Contract"]
    client_contract = constants["Client_Contract"]
    client_owner = constants["Client_Owner"]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    registration_deposit = constants["Registration_Deposit"]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    node_contract_0 = TestKhronusNode.deploy(coordinator_contract.address, {'from':node_owner_0})
    node_contract_1 = TestKhronusNode.deploy(coordinator_contract.address, {'from':node_owner_1})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_1.address,{'from':node_owner_1})
    # Set Test
    txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {'from':escrow_depositor})
    events_of_interest = txt.events['AlertDispatched'], txt.events['Transfer']
    #Test Log
    current_time = datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime()
    data = {'Test':'setKhronRequest_Two_Nodes','TestTime':current_time, 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address, "Nodes":[node_contract_0.address, node_contract_1.address]}, "Events":events_of_interest}
    logger(data)
    # No Assertion
    assert (events_of_interest[0]["assignedNode"][0] == node_contract_0.address) and events_of_interest[0]["assignedNode"][1] == node_contract_1.address
    assert (events_of_interest[1][1]['to'] == node_contract_0.address) and events_of_interest[1][2]['to'] == node_contract_1.address

def test_sendKhronRequest_one_node_available(constants, current_utc_timestamp): 
    # Set up constants for testing
    token_contract = constants["Token_Contract"]
    coordinator_contract = constants["Coordinator_Contract"]
    client_contract = constants["Client_Contract"]
    client_owner = constants["Client_Owner"]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    node_owner_0 = accounts[4]
    registration_deposit = constants["Registration_Deposit"]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    node_contract_0 = TestKhronusNode.deploy(coordinator_contract.address, {'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    # Set Test
    txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {'from':escrow_depositor})
    events_of_interest = txt.events['AlertDispatched']
    #Test Log
    current_time = datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime()
    data = {'Test':'setKhronRequest_One_Node','TestTime':current_time, 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address, "Node":node_contract_0.address}, "Events":events_of_interest}
    logger(data)
    # Assertion
    assert (events_of_interest["assignedNode"][0] == events_of_interest["assignedNode"][1]) and events_of_interest["assignedNode"][0] == node_contract_0.address

def test_sendKhronRequest_no_nodes_available_error(constants, current_utc_timestamp): 
    # Set up constants for testing
    token_contract = constants["Token_Contract"]
    coordinator_contract = constants["Coordinator_Contract"]
    client_contract = constants["Client_Contract"]
    client_owner = constants["Client_Owner"]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    registration_deposit = constants["Registration_Deposit"]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    # Set test
    message = ""
    current_time = datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime()
    try:
        txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {'from':escrow_depositor})
        #Test Log
        data = {'Test':'setKhronRequest','TestTime':current_time, 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address}, "Events":dict(txt.events)}
        logger(data)
        # No Assertion
    except Exception as e:
        data = {'Test':'setKhronRequest_Exception_no_nodes','TestTime':current_time, 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address}, "Exception":e.message}
        logger(data)
        message = e.message
    assert coordinator_contract.nodeCorrelative() == 0
    assert message == 'VM Exception while processing transaction: revert No nodes available to serve requests'

def test_multiple_call_credits_below_limit(constants, current_utc_timestamp):
    # Set up constants for testing
    token_contract = constants["Token_Contract"]
    coordinator_contract = constants["Coordinator_Contract"]
    client_contract = constants["Client_Contract"]
    client_owner = constants["Client_Owner"]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    registration_deposit = constants["Registration_Deposit"]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    node_contract_0 = TestKhronusNode.deploy(coordinator_contract.address, {'from':node_owner_0})
    node_contract_1 = TestKhronusNode.deploy(coordinator_contract.address, {'from':node_owner_1})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_1.address,{'from':node_owner_1})
    txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent,{'from':escrow_depositor})
    coordinator_contract.withdrawFromContract(client_contract.address,registration_deposit,{'from':client_owner})
    message = ""
    try: 
        txt_01 = client_contract.openEscrow(escrow_beneficiary, timestamp, agent,{'from':escrow_depositor})
    except Exception as e:
        message = e.message
        data = {"Test":"Credits Below Limit", "Exception":message}
        logger(data)
    assert message == 'VM Exception while processing transaction: revert Client contract balance below minimum balance'

def test_multiple_withdrawal(constants, current_utc_timestamp):
    # Set up constants for testing
    token_contract = constants["Token_Contract"]
    coordinator_contract = constants["Coordinator_Contract"]
    client_contract = constants["Client_Contract"]
    client_owner = constants["Client_Owner"]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    registration_deposit = constants["Registration_Deposit"]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    client_owner_base_balance = token_contract.balanceOf(client_owner.address)
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    node_contract_0 = TestKhronusNode.deploy(coordinator_contract.address, {'from':node_owner_0})
    node_contract_1 = TestKhronusNode.deploy(coordinator_contract.address, {'from':node_owner_1})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_1.address,{'from':node_owner_1})
    txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent,{'from':escrow_depositor})
    coordinator_contract.withdrawFromContract(client_contract.address,registration_deposit,{'from':client_owner})
    coordinator_contract.withdrawBalance({'from':client_owner})
    data = {"Test":"Withdrawal from client owner"}
    assert token_contract.balanceOf(client_owner.address) == client_owner_base_balance
