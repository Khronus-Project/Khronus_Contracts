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
    token_contract = constants["Token_Contract"]
    coordinator_contract = constants["Coordinator_Contract"]
    client_contract = constants["Client_Contract"]
    nodeContract_0 = constants["Node_Contracts"][0]
    nodeContract_1 = constants["Node_Contracts"][1]
    operators = constants["Node_Operators"]
    khron_oracle = constants["Khron_Oracle"]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp+(minutes_to_clearance*60)
    escrow_amount = 1*10**18
    agent = accounts[0]
    mock_node = accounts[0]
    khron_eth_price = khron_oracle.getLatestPriceKhronETH()
    operator_markup = coordinator_contract.getOperatorMarkup()
    # Set environment for testing
    eth_balance_beneficiary = escrow_beneficiary.balance()
    operator_0_t0_khrbalance = coordinator_contract.getOperatorBalance({"from":operators[0].address}) 
    node_0_t0_ethbalance = mock_node.balance()
    txt_set_escrow = client_contract.openEscrow(escrow_beneficiary, timestamp, agent,{'from':escrow_depositor, 'value':escrow_amount})
    escrow_ID = txt_set_escrow.return_value
    #txt_escrow_status = client_contract.agentInput(escrow_ID,True, {'from':agent})
    alert_ID = txt_set_escrow.events['AlertDispatched']['alertID']
    # Set Test
    sleep(minutes_to_clearance*60)
    txt_serve_alert = nodeContract_0.fulfillAlert(alert_ID, {'from':mock_node, "gas_price":"1 gwei"})
    events_of_interest = txt_serve_alert.events["AlertCompensated"]
    consumed_gas_fee = (node_0_t0_ethbalance - mock_node.balance()) 
    compensation_khron = coordinator_contract.getOperatorBalance({"from":operators[0].address}) /1e18
    expected_eth = consumed_gas_fee * 1.1
    expected_khron = (expected_eth / khron_eth_price )
    band_of_tolerance = (15000 * txt_serve_alert.gas_price) / khron_eth_price
    difference_khron = expected_khron - compensation_khron
    testing_data = {'Test':'KhronAlertOperations','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address, "Nodes":[nodeContract_0.address, nodeContract_1.address]}}
    #Test Log
    data = {"transaction_gas":txt_serve_alert.gas_used, "gas_fee":consumed_gas_fee, "compensation_khron":compensation_khron, "expected_khron":expected_khron, "difference_khron":difference_khron, "band_of_tolerance":band_of_tolerance, "Events":events_of_interest}
    logger(data)
    # Assertion
    #assert escrow_beneficiary.balance() == eth_balance_beneficiary + escrow_amount
    assert compensation_khron ==  expected_khron

