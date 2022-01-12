import pytest
from datetime import datetime, timezone
from brownie import accounts
from testing_utils import logger, khron_constants_operations
from time import sleep

@pytest.fixture
def constants():
    return khron_constants_operations()

@pytest.fixture
def current_utc_timestamp():
    return int(datetime.now(timezone.utc).timestamp())

def test_alert_operation_happyPath(constants, current_utc_timestamp): 
    # Set up constants for testing
    logger("started test propper")
    token_contract = constants["Token_Contract"]
    coordinator_contract = constants["Coordinator_Contract"]
    client_contract = constants["Client_Contract"]
    nodeContract_0 = constants["Node_Contracts"][0]
    nodeContract_1 = constants["Node_Contracts"][1]
    benchmark_client = constants["Benchmark_Client"]
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    minutes_to_clearance = 1
    timestamp = current_utc_timestamp+(minutes_to_clearance*60)
    escrow_amount = 1*10**18
    agent = accounts[0]
    mock_node = accounts[0]
    # Set environment for testing
    eth_balance_beneficiary = escrow_beneficiary.balance()
    #khron_balance_node_0 = token_contract.balanceOf(nodeContract_0.address) 
    txt_set_benchmark = benchmark_client.setTab(timestamp, {'from':escrow_depositor})
    logger("tab set")
    # / txt_set_escrow = client_contract.openEscrow(escrow_beneficiary, timestamp, agent,{'from':escrow_depositor, 'value':escrow_amount})
    logger("escrow opened")
    sleep(minutes_to_clearance*60)
    benchmark_ID = txt_set_benchmark.return_value
    benchmark_alert_ID = txt_set_benchmark.events['AlertDispatched']['alertID']
    # / escrow_ID = txt_set_escrow.return_value
    # /alert_ID = txt_set_escrow.events['AlertDispatched']['alertID']
    #events_of_interest = txt_escrow_status.events["ConditionChanged"]
    # Set Test
    # /escrow_txt_serve_alert = nodeContract_0.fulfillAlert(alert_ID, {'from':mock_node, "gas_price":"1 gwei"})
    benchmark_txt_serve_alert = nodeContract_0.fulfillAlert(benchmark_alert_ID, {'from':mock_node, "gas_price":"1 gwei"})
    benchmark_txt_serve_alert_02 = nodeContract_1.fulfillAlert(benchmark_alert_ID, {'from':mock_node, "gas_price":"1 gwei"})
    #Test Log
    #data = {'Test':'KhronAlertOperations','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Client":client_contract.address, "Nodes":[nodeContract_0.address, nodeContract_1.address]}, "transaction":txt_serve_alert,"Events":txt_serve_alert.events}
    #data = {"transaction_id":escrow_tx_id,"transaction_gas":escrow_tx_gas_used,"Events_Set_Escrow":txt_set_escrow.events,"Events_Fulfill":escrow_txt_serve_alert.events}
    logger("fulfilled alerts")
    # /escrow_tx_id=escrow_txt_serve_alert.txid
    # / escrow_tx_gas_used=escrow_txt_serve_alert.gas_used
    # /estimated_escrow_serve_gas = escrow_txt_serve_alert.events["WorkflowCompleted"]["partialGas"]
    # /total_escrow_serve_gas = escrow_txt_serve_alert.events["RequestServed"]["totalGas"]
    benchmark_tx_id=benchmark_txt_serve_alert.txid
    benchmark_tx_gas_used=benchmark_txt_serve_alert.gas_used
    estimated_benchmark_serve_gas = benchmark_txt_serve_alert.events["WorkflowCompleted"]["partialGas"]
    total_benchmark_serve_gas = benchmark_txt_serve_alert.events["RequestServed"]["totalGas"]
    # / data = {"transaction_id":escrow_tx_id,"transaction_gas":escrow_tx_gas_used, "estimated_gas":estimated_escrow_serve_gas, "gas_difference_escrow":escrow_tx_gas_used-estimated_escrow_serve_gas,"total_gas":total_escrow_serve_gas}
    data_benchmark = {"b_transaction_id":benchmark_tx_id,"b_transaction_gas":benchmark_tx_gas_used, "b_estimated_gas":estimated_benchmark_serve_gas, "b_gas_difference_escrow":benchmark_tx_gas_used-estimated_benchmark_serve_gas, "total_gas":total_benchmark_serve_gas}
    logger("Data regarding the use of gas for set alerts")
    # /logger({"total_open_escrow_gas":txt_set_escrow.gas_used,"escrow_set_alert_gas":txt_set_escrow.events["AlertDispatched"]["gasCost"],"difference":txt_set_escrow.gas_used-txt_set_escrow.events["AlertDispatched"]["gasCost"]})
    logger({"b_total_open_tab_gas":txt_set_benchmark.gas_used,"b_set_alert_gas":txt_set_benchmark.events["AlertDispatched"]["gasCost"],"difference":txt_set_benchmark.gas_used-txt_set_benchmark.events["AlertDispatched"]["gasCost"]})
    logger("Data regarding the use of gas for fulfill alerts")
    #logger(data)
    logger(data_benchmark)
    #logger("Data regarding second node response")
    sleep(60)
    logger(dir(benchmark_txt_serve_alert_02))
    # Assertion
    assert escrow_beneficiary.balance() == eth_balance_beneficiary + escrow_amount
    #assert token_contract.balanceOf(nodeContract_0.address) == khron_balance_node_0 + (call_price/2)

