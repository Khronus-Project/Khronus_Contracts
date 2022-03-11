import pytest
from datetime import datetime, timezone
from brownie import accounts
from testing_utils import logger, khron_contants_operations_proxied
from time import sleep

@pytest.fixture
def constants():
    return khron_contants_operations_proxied()

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
    gas_tolerance = constants["Gas_Tolerance"]
    mock_node_0 = accounts[9]
    mock_node_1 = accounts[8]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp+(minutes_to_clearance*60)
    escrow_amount = 1*10**18
    agent = accounts[0]
    testing_data = {'Test':'KhronAlertOperations','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address, "Nodes":[nodeContract_0.address, nodeContract_1.address]}}
    # Set environment for testing
    khron_eth_price = khron_oracle.getLatestPriceKhronETH()
    khron_band_of_tolerance = ((gas_tolerance *1.1) * 1000000000) / (khron_eth_price /1e18)
    eth_balance_beneficiary = escrow_beneficiary.balance()
    node_0_t0_ethbalance = mock_node_0.balance()
    node_1_t0_ethbalance = mock_node_1.balance()
    txt_set_escrow = client_contract.openEscrow(escrow_beneficiary, timestamp, agent,{'from':escrow_depositor, 'value':escrow_amount})
    escrow_ID = txt_set_escrow.return_value
    txt_escrow_status = client_contract.agentInput(escrow_ID,True, {'from':agent})
    alert_ID = txt_set_escrow.events['AlertDispatched']['alertID']
    khron_balance_client = coordinator_contract.getKhronBalanceOf(client_contract.address) 
    # Set Test
    sleep(minutes_to_clearance*60)
    # Primary Alert
    txt_serve_alert_0 = nodeContract_0.fulfillAlert(alert_ID, {'from':mock_node_0, "gas_price":"1 gwei"})
    events_of_interest_0 = txt_serve_alert_0.events["AlertCompensated"]
    consumed_gas_fee_0 = (node_0_t0_ethbalance - mock_node_0.balance()) 
    compensation_khron_0 = coordinator_contract.getKhronBalanceOf(operators[0].address) 
    expected_eth_0 = consumed_gas_fee_0 + ((consumed_gas_fee_0 * 10 )/100)
    expected_khron_0 = (expected_eth_0 / (khron_eth_price / 1e18) )
    difference_khron_0 = expected_khron_0 - compensation_khron_0
    data_0 = {"transaction_gas":txt_serve_alert_0.gas_used, "gas_fee":consumed_gas_fee_0,"expected_eth":expected_eth_0,"compensation_khron":compensation_khron_0, "expected_khron":expected_khron_0, "difference_khron":difference_khron_0, "band_of_tolerance":khron_band_of_tolerance, "Events":events_of_interest_0}
    # Secondary Alert
    txt_serve_alert_1 = nodeContract_1.fulfillAlert(alert_ID, {'from':mock_node_1, "gas_price":"1 gwei"})
    events_of_interest_1 = [txt_serve_alert_1.events["AlertCompensated"],txt_serve_alert_1.events["AlertFulfilled"]]
    consumed_gas_fee_1 = (node_1_t0_ethbalance - mock_node_1.balance()) 
    compensation_khron_1 = coordinator_contract.getKhronBalanceOf(operators[1].address,{"from":operators[1].address}) 
    expected_eth_1 = consumed_gas_fee_1 + ((consumed_gas_fee_1 * 10)/100)
    expected_khron_1 = ((expected_eth_1 ) / (khron_eth_price / 1e18) )
    difference_khron_1 = expected_khron_1 - compensation_khron_1
    data_1 = {"transaction_gas":txt_serve_alert_1.gas_used, "gas_fee":consumed_gas_fee_1,"expected_eth":expected_eth_1, "compensation_khron":compensation_khron_1, "expected_khron":expected_khron_1, "difference_khron":difference_khron_1, "band_of_tolerance":khron_band_of_tolerance, "Events":events_of_interest_1}
    #Test Log
    logger("Testing Happy Path")
    logger(testing_data)
    logger(data_0)
    logger(data_1)
    # Assertion
    assert coordinator_contract.getKhronBalanceOf(client_contract.address) == khron_balance_client - (compensation_khron_0 + compensation_khron_1)
    assert escrow_beneficiary.balance() == eth_balance_beneficiary + escrow_amount
    assert compensation_khron_0 <= expected_khron_0 + khron_band_of_tolerance and  compensation_khron_0 >= expected_khron_0  
    assert compensation_khron_1 <= expected_khron_1 + khron_band_of_tolerance and  compensation_khron_1 >= expected_khron_1 

def test_alert_operation_serve_twice_same_node(constants, current_utc_timestamp): 
    # Set up constants for testing
    token_contract = constants["Token_Contract"]
    coordinator_contract = constants["Coordinator_Contract"]
    client_contract = constants["Client_Contract"]
    nodeContract_0 = constants["Node_Contracts"][0]
    nodeContract_1 = constants["Node_Contracts"][1]
    operators = constants["Node_Operators"]
    khron_oracle = constants["Khron_Oracle"]
    gas_tolerance = constants["Gas_Tolerance"]
    mock_node_0 = accounts[9]
    mock_node_1 = accounts[8]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp+(minutes_to_clearance*60)
    escrow_amount = 1*10**18
    agent = accounts[0]
    testing_data = {'Test':'KhronAlertOperations','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address, "Nodes":[nodeContract_0.address, nodeContract_1.address]}}
    # Set environment for testing
    khron_eth_price = khron_oracle.getLatestPriceKhronETH()
    khron_band_of_tolerance = ((gas_tolerance *1.1) * 1000000000) / (khron_eth_price /1e18)
    eth_balance_beneficiary = escrow_beneficiary.balance()
    node_0_t0_ethbalance = mock_node_0.balance()
    node_1_t0_ethbalance = mock_node_1.balance()
    txt_set_escrow = client_contract.openEscrow(escrow_beneficiary, timestamp, agent,{'from':escrow_depositor, 'value':escrow_amount})
    escrow_ID = txt_set_escrow.return_value
    txt_escrow_status = client_contract.agentInput(escrow_ID,True, {'from':agent})
    alert_ID = txt_set_escrow.events['AlertDispatched']['alertID']
    khron_balance_client = coordinator_contract.getKhronBalanceOf(client_contract.address) 
    # Set Test
    sleep(minutes_to_clearance*60)
    # Primary Alert
    txt_serve_alert_0 = nodeContract_0.fulfillAlert(alert_ID, {'from':mock_node_0, "gas_price":"1 gwei"})
    events_of_interest_0 = txt_serve_alert_0.events["AlertCompensated"]
    consumed_gas_fee_0 = (node_0_t0_ethbalance - mock_node_0.balance()) 
    compensation_khron_0 = coordinator_contract.getKhronBalanceOf(operators[0].address,{"from":operators[0].address}) 
    expected_eth_0 = consumed_gas_fee_0 + ((consumed_gas_fee_0 * 10 )/100)
    expected_khron_0 = (expected_eth_0 / (khron_eth_price / 1e18) )
    difference_khron_0 = expected_khron_0 - compensation_khron_0
    data_0 = {"transaction_gas":txt_serve_alert_0.gas_used, "gas_fee":consumed_gas_fee_0,"expected_eth":expected_eth_0,"compensation_khron":compensation_khron_0, "expected_khron":expected_khron_0, "difference_khron":difference_khron_0, "band_of_tolerance":khron_band_of_tolerance, "Events":events_of_interest_0}
    # Secondary Alert
    try:    
        txt_serve_alert_1 = nodeContract_0.fulfillAlert(alert_ID, {'from':mock_node_0, "gas_price":"1 gwei"})
        events_of_interest_1 = [txt_serve_alert_1.events["AlertCompensated"],txt_serve_alert_1.events["AlertFulfilled"]]
        consumed_gas_fee_1 = (consumed_gas_fee_0 - mock_node_0.balance()) 
        compensation_khron_1 = coordinator_contract.getKhronBalanceOf(operators[0].address,{"from":operators[0].address}) - compensation_khron_0 
        expected_eth_1 = consumed_gas_fee_1 + ((consumed_gas_fee_1 * 10)/100)
        expected_khron_1 = ((expected_eth_1 ) / (khron_eth_price / 1e18) )
        difference_khron_1 = expected_khron_1 - compensation_khron_1
        data_1 = {"transaction_gas":txt_serve_alert_1.gas_used, "gas_fee":consumed_gas_fee_1,"expected_eth":expected_eth_1, "compensation_khron":compensation_khron_1, "expected_khron":expected_khron_1, "difference_khron":difference_khron_1, "band_of_tolerance":khron_band_of_tolerance, "Events":events_of_interest_1}
    except Exception as e:
        data_1 = e.message
        #Test Log
    logger("Testing Node Double Dipping")
    logger(testing_data)
    logger(data_0)
    logger(data_1)
    # Assertion
    assert coordinator_contract.getKhronBalanceOf(client_contract.address) == khron_balance_client - (compensation_khron_0 )
    assert escrow_beneficiary.balance() == eth_balance_beneficiary + escrow_amount
    assert compensation_khron_0 <= expected_khron_0 + khron_band_of_tolerance and  compensation_khron_0 >= expected_khron_0  
    assert data_1 == "VM Exception while processing transaction: revert Alert was already served by this node"


def test_operator_withdrawal_happyPath(constants, current_utc_timestamp): 
    # Set up constants for testing
    token_contract = constants["Token_Contract"]
    coordinator_contract = constants["Coordinator_Contract"]
    client_contract = constants["Client_Contract"]
    nodeContract_0 = constants["Node_Contracts"][0]
    nodeContract_1 = constants["Node_Contracts"][1]
    operators = constants["Node_Operators"]
    khron_oracle = constants["Khron_Oracle"]
    gas_tolerance = constants["Gas_Tolerance"]
    mock_node_0 = accounts[9]
    mock_node_1 = accounts[8]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp+(minutes_to_clearance*60)
    escrow_amount = 1*10**18
    agent = accounts[0]
    testing_data = {'Test':'KhronAlertOperations','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address, "Nodes":[nodeContract_0.address, nodeContract_1.address]}}
    # Set environment for testing
    khron_eth_price = khron_oracle.getLatestPriceKhronETH()
    khron_band_of_tolerance = ((gas_tolerance *1.1) * 1000000000) / (khron_eth_price /1e18)
    eth_balance_beneficiary = escrow_beneficiary.balance()
    node_0_t0_ethbalance = mock_node_0.balance()
    node_1_t0_ethbalance = mock_node_1.balance()
    txt_set_escrow = client_contract.openEscrow(escrow_beneficiary, timestamp, agent,{'from':escrow_depositor, 'value':escrow_amount})
    escrow_ID = txt_set_escrow.return_value
    txt_escrow_status = client_contract.agentInput(escrow_ID,True, {'from':agent})
    alert_ID = txt_set_escrow.events['AlertDispatched']['alertID']
    khron_balance_client = coordinator_contract.getKhronBalanceOf(client_contract.address) 
    # Set Test
    sleep(minutes_to_clearance*60)
    # Primary Alert
    txt_serve_alert_0 = nodeContract_0.fulfillAlert(alert_ID, {'from':mock_node_0, "gas_price":"1 gwei"})
    events_of_interest_0 = txt_serve_alert_0.events["AlertCompensated"]
    consumed_gas_fee_0 = (node_0_t0_ethbalance - mock_node_0.balance()) 
    compensation_khron_0 = coordinator_contract.getKhronBalanceOf(operators[0].address) 
    expected_eth_0 = consumed_gas_fee_0 + ((consumed_gas_fee_0 * 10 )/100)
    expected_khron_0 = (expected_eth_0 / (khron_eth_price / 1e18) )
    difference_khron_0 = expected_khron_0 - compensation_khron_0
    coordinator_contract.withdrawBalance({"from":operators[0]})
    data_0 = {"transaction_gas":txt_serve_alert_0.gas_used, "gas_fee":consumed_gas_fee_0,"expected_eth":expected_eth_0,"compensation_khron":compensation_khron_0, "expected_khron":expected_khron_0, "difference_khron":difference_khron_0, "band_of_tolerance":khron_band_of_tolerance, "Events":events_of_interest_0}
    # Secondary Alert
    txt_serve_alert_1 = nodeContract_1.fulfillAlert(alert_ID, {'from':mock_node_1, "gas_price":"1 gwei"})
    events_of_interest_1 = [txt_serve_alert_1.events["AlertCompensated"],txt_serve_alert_1.events["AlertFulfilled"]]
    consumed_gas_fee_1 = (node_1_t0_ethbalance - mock_node_1.balance()) 
    compensation_khron_1 = coordinator_contract.getKhronBalanceOf(operators[1].address,{"from":operators[1].address}) 
    expected_eth_1 = consumed_gas_fee_1 + ((consumed_gas_fee_1 * 10)/100)
    expected_khron_1 = ((expected_eth_1 ) / (khron_eth_price / 1e18) )
    difference_khron_1 = expected_khron_1 - compensation_khron_1
    coordinator_contract.withdrawBalance({"from":operators[1]})
    data_1 = {"transaction_gas":txt_serve_alert_1.gas_used, "gas_fee":consumed_gas_fee_1,"expected_eth":expected_eth_1, "compensation_khron":compensation_khron_1, "expected_khron":expected_khron_1, "difference_khron":difference_khron_1, "band_of_tolerance":khron_band_of_tolerance, "Events":events_of_interest_1}
    #Test Log
    logger("Testing Withdrawal Happy Path")
    logger(testing_data)
    logger(data_0)
    logger(data_1)
    # Assertion
    assert token_contract.balanceOf(operators[0].address) == compensation_khron_0
    assert token_contract.balanceOf(operators[1].address) == compensation_khron_1
