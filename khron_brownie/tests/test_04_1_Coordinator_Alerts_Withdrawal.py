import pytest
from datetime import datetime, timezone
from brownie import accounts
from testing_utils import logger, khron_contants_operations01
from time import sleep

@pytest.fixture
def constants01():
    return khron_contants_operations01()

@pytest.fixture
def current_utc_timestamp():
    return int(datetime.now(timezone.utc).timestamp())


def test_operator_withdrawal_happyPath(constants01, current_utc_timestamp): 
    # Set up constants for testing
    coordinator_contract = constants01["Coordinator_Contract"]
    client_contract = constants01["Client_Contract"]
    nodeContract_0 = constants01["Node_Contracts"][0]
    nodeContract_1 = constants01["Node_Contracts"][1]
    operators = constants01["Node_Operators"]
    mock_node_0 = accounts[9]
    mock_node_1 = accounts[8]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp+(minutes_to_clearance*60)
    escrow_amount = 1*10**18
    agent = accounts[0]
    testing_data = {'Test':'KhronAlertOperations','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Coordinator":coordinator_contract.address,"Client":client_contract.address, "Nodes":[nodeContract_0.address, nodeContract_1.address]}}
    # Set environment for testing
    node_0_t0_ethbalance = mock_node_0.balance()
    node_1_t0_ethbalance = mock_node_1.balance()
    txt_set_escrow = client_contract.openEscrow(escrow_beneficiary, timestamp, agent,{'from':escrow_depositor, 'value':escrow_amount})
    escrow_ID = txt_set_escrow.return_value
    txt_escrow_status = client_contract.agentInput(escrow_ID,True, {'from':agent})
    alert_ID = txt_set_escrow.events['AlertDispatched']['alertID']
    # Set Test
    sleep(minutes_to_clearance*60)
    # Primary Alert
    txt_serve_alert_0 = nodeContract_0.fulfillAlert(alert_ID, {'from':mock_node_0, "gas_price":"1 gwei"})
    events_of_interest_0 = txt_serve_alert_0.events["AlertCompensated"]
    consumed_gas_fee_0 = (node_0_t0_ethbalance - mock_node_0.balance())
    expected_eth_0 = consumed_gas_fee_0 + ((consumed_gas_fee_0 * 10 )/100)
    coordinator_contract.withdrawBalance(expected_eth_0,{"from":operators[0]})
    data_0 = {"transaction_gas":txt_serve_alert_0.gas_used, "gas_fee":consumed_gas_fee_0,"expected_eth":expected_eth_0,"Events":events_of_interest_0}
    # Secondary Alert
    txt_serve_alert_1 = nodeContract_1.fulfillAlert(alert_ID, {'from':mock_node_1, "gas_price":"1 gwei"})
    events_of_interest_1 = [txt_serve_alert_1.events["AlertCompensated"],txt_serve_alert_1.events["AlertFulfilled"]]
    consumed_gas_fee_1 = (node_1_t0_ethbalance - mock_node_1.balance())
    expected_eth_1 = consumed_gas_fee_1 + ((consumed_gas_fee_1 * 10)/100)
    coordinator_contract.withdrawBalance(expected_eth_1,{"from":operators[1]})
    data_1 = {"transaction_gas":txt_serve_alert_1.gas_used, "gas_fee":consumed_gas_fee_1,"expected_eth":expected_eth_1, "Events":events_of_interest_1}
    #Test Log
    logger("Testing Withdrawal Happy Path")
    logger(testing_data)
    logger(data_0)
    logger(data_1)