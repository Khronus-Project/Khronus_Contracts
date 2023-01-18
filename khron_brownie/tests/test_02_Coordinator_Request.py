import pytest
from datetime import datetime, timezone
from brownie import accounts, TestKhronusNode01
from testing_utils import logger, khron_constants_client01

@pytest.fixture
def constants01():
    return khron_constants_client01()

@pytest.fixture
def current_utc_timestamp():
    return int(datetime.now(timezone.utc).timestamp())

def test_sendKhronRequest_happyPath01(constants01, current_utc_timestamp): 
    # Set up constants01 for testing
    coordinator_contract = constants01["Coordinator_Contract"]
    client_contract = constants01["Client_Contract"]
    client_owner = constants01["Client_Owner"]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    registration_deposit = constants01["Registration_Deposit"]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    coordinator_contract.registerClient(client_contract.address, {'from':client_owner, 'value':registration_deposit})
    node_contract_0 = TestKhronusNode01.deploy(coordinator_contract.address, {'from':node_owner_0})
    node_contract_1 = TestKhronusNode01.deploy(coordinator_contract.address, {'from':node_owner_1})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_1.address,{'from':node_owner_1})
    logger(f'Client balance is {coordinator_contract.getBalanceOf(client_contract.address)/1e18} minimum balance is {coordinator_contract.getMinimumClientBalance()/1e18}')
    # Set Test
    txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {'from':escrow_depositor})
    events_of_interest = txt.events['AlertDispatched']
    #Test Log
    current_time = datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime()
    data = {'Test':'setKhronRequest_Two_NodesV01','TestTime':current_time, 'TestingAddresses':{"Coordinator":coordinator_contract.address,"Client":client_contract.address, "Nodes":[node_contract_0.address, node_contract_1.address]}, "Events":events_of_interest}
    logger(data)
    # No Assertion
    assert (events_of_interest[0]["assignedNode"][0] == node_contract_0.address) and events_of_interest[0]["assignedNode"][1] == node_contract_1.address

def test_sendKhronRequest_one_node_available(constants01, current_utc_timestamp): 
    # Set up constants01 for testing
    coordinator_contract = constants01["Coordinator_Contract"]
    client_contract = constants01["Client_Contract"]
    client_owner = constants01["Client_Owner"]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    node_owner_0 = accounts[4]
    registration_deposit = constants01["Registration_Deposit"]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    coordinator_contract.registerClient(client_contract.address, {'from':client_owner, 'value':registration_deposit})
    node_contract_0 = TestKhronusNode01.deploy(coordinator_contract.address, {'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    # Set Test
    txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {'from':escrow_depositor})
    events_of_interest = txt.events['AlertDispatched']
    #Test Log
    current_time = datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime()
    data = {'Test':'setKhronRequest_One_Node','TestTime':current_time, 'TestingAddresses':{ "Coordinator":coordinator_contract.address,"Client":client_contract.address, "Node":node_contract_0.address}, "Events":events_of_interest}
    logger(data)
    # Assertion
    assert (events_of_interest["assignedNode"][0] == events_of_interest["assignedNode"][1]) and events_of_interest["assignedNode"][0] == node_contract_0.address

def test_sendKhronRequest_no_nodes_available_error(constants01, current_utc_timestamp): 
    # Set up constants01 for testing
    coordinator_contract = constants01["Coordinator_Contract"]
    client_contract = constants01["Client_Contract"]
    client_owner = constants01["Client_Owner"]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    registration_deposit = constants01["Registration_Deposit"]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    coordinator_contract.registerClient(client_contract.address, {'from':client_owner, 'value':registration_deposit})
    # Set test
    message = ""
    current_time = datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime()
    try:
        txt = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {'from':escrow_depositor})
        #Test Log
        data = {'Test':'setKhronRequest','TestTime':current_time, 'TestingAddresses':{"Coordinator":coordinator_contract.address,"Client":client_contract.address}, "Events":dict(txt.events)}
        logger(data)
        # No Assertion
    except Exception as e:
        data = {'Test':'setKhronRequest_Exception_no_nodes','TestTime':current_time, 'TestingAddresses':{"Coordinator":coordinator_contract.address,"Client":client_contract.address}, "Exception":e.message}
        logger(data)
        message = e.message
    assert coordinator_contract.nodeCorrelative() == 0
    assert message == 'VM Exception while processing transaction: revert No nodes available to serve requests'


def test_multiple_call_credits_below_limit(constants01, current_utc_timestamp):
    # Set up constants01 for testing
    coordinator_contract = constants01["Coordinator_Contract"]
    client_contract = constants01["Client_Contract"]
    client_owner = constants01["Client_Owner"]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    registration_deposit = constants01["Registration_Deposit"]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp +(minutes_to_clearance*60)
    agent = accounts[0]
    # Set environment for testing
    coordinator_contract.registerClient(client_contract.address, {'from':client_owner, 'value':registration_deposit})
    node_contract_0 = TestKhronusNode01.deploy(coordinator_contract.address, {'from':node_owner_0})
    node_contract_1 = TestKhronusNode01.deploy(coordinator_contract.address, {'from':node_owner_1})
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

