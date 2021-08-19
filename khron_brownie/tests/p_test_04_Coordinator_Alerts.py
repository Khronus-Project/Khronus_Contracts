import pytest
from datetime import datetime, timezone
from brownie import accounts
from testing_utils import logger, khron_contants_operations
from time import sleep

@pytest.fixture
def constants():
    return khron_contants_operations()

@pytest.fixture
def current_utc_timestamp():
    return int(datetime.now(timezone.utc).timestamp())

def test_alert_operation_happyPath(constants, current_utc_timestamp): 
    # Set up constants for testing
    token_contract = constants[0]
    coordinator_contract = constants[1]
    client_contract = constants[2]
    nodeContract_0 = constants[3]
    nodeContract_1 = constants[4]
    call_price = constants[9]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp+(minutes_to_clearance*60)
    escrow_amount = 1*10**18
    agent = accounts[0]
    # Set environment for testing
    eth_balance_beneficiary = escrow_beneficiary.balance()
    khron_balance_node_0 = token_contract.balanceOf(nodeContract_0.address) 
    txt_set_escrow = client_contract.openEscrow(escrow_beneficiary, timestamp, agent,{'from':escrow_depositor, 'value':escrow_amount})
    escrow_ID = txt_set_escrow.return_value
    txt_escrow_status = client_contract.agentInput(escrow_ID,True, {'from':agent})
    events_of_interest = txt_escrow_status.events["ConditionChanged"]
    # Set Test
    sleep(60)
    #Test Log
    data = {'Test':'KhronAlertOperations','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address, "Nodes":[nodeContract_0.address, nodeContract_1.address]}, "Events":events_of_interest}
    logger(data)
    # No Assertion
    assert escrow_beneficiary.balance() == eth_balance_beneficiary + escrow_amount
    assert token_contract.balanceOf(nodeContract_0.address) == khron_balance_node_0 + (call_price/2)


