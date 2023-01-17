from brownie import accounts, KhronusCoordinatorV01, EscrowInfrastructure, BasicClient, TestKhronusNode01
from time import sleep
from datetime import datetime, timezone
from scripts.scripts_utils import Served_Alert_Tx;
import json

def current_closest_minute():
    current_timestamp = int(datetime.now(timezone.utc).timestamp())
    extra_seconds = current_timestamp % 60
    closest_minute = current_timestamp - extra_seconds
    return closest_minute

def main():
    # Constants
    escrow_depositor = accounts[2]
    escrow_beneficiary = accounts[3]
    agent = accounts[0]
    mock_node_0 = accounts[0]
    mock_node_1 = accounts[9]
    timestamp = current_closest_minute() + 60
    with open ('../contract_library/contract_addresses_local.json') as f:
        addresses = json.load(f)
    coordinator_contract = KhronusCoordinatorV01.at(addresses["KhronusCoordinator"])
    client_contract = EscrowInfrastructure.at(addresses["KhronusClient"])
    benchmark_contract = BasicClient.at(addresses["KhronusBenchmark"])
    node_contract_0 = TestKhronusNode01.at(addresses["KhronusNode_0"])
    node_contract_1 = TestKhronusNode01.at(addresses["KhronusNode_1"])
    txt_request_client_1 = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {"from":escrow_depositor, "value":"1 ether"})
    txt_request_benchmark_1 = benchmark_contract.setTab(timestamp,{"from":escrow_depositor})
    alert_ID_client_1 = txt_request_client_1.events['AlertDispatched']['alertID']
    alert_ID_benchmark_1 = txt_request_benchmark_1.events['AlertDispatched']['alertID']
    sleep(60)
    print(f"Alerts are being fulfilled at {current_closest_minute()}")
    try: 
        serve_alert_client_1 =node_contract_0.fulfillAlert(alert_ID_client_1, {'from':mock_node_0,  "gas_price":"1 gwei"})
        served_alert_client_1 = Served_Alert_Tx(serve_alert_client_1, "client_main_first")
        re_serve_alert_client_1 =node_contract_1.fulfillAlert(alert_ID_client_1, {'from':mock_node_1,  "gas_price":"1 gwei"})
        re_served_alert_client_1 = Served_Alert_Tx(re_serve_alert_client_1, "client_sec_first")
        serve_alert_benchmark_1 =node_contract_0.fulfillAlert(alert_ID_benchmark_1, {'from':mock_node_0,  "gas_price":"1 gwei"})
        served_alert_benchmark_1 = Served_Alert_Tx(serve_alert_benchmark_1, "benchmark_main_first")
        re_serve_alert_benchmark_1 =node_contract_1.fulfillAlert(alert_ID_benchmark_1, {'from':mock_node_1,  "gas_price":"1 gwei"})
        re_served_alert_benchmark_1 = Served_Alert_Tx(re_serve_alert_benchmark_1, "benchmark_sec_first")
    except Exception as e:
        print(e)
    timestamp = current_closest_minute() + 60
    txt_request_client_2 = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {"from":escrow_depositor, "value":"1 ether"})
    txt_request_benchmark_2 = benchmark_contract.setTab(timestamp,{"from":escrow_depositor})
    alert_ID_client_2 = txt_request_client_2.events['AlertDispatched']['alertID']
    alert_ID_benchmark_2 = txt_request_benchmark_2.events['AlertDispatched']['alertID']
    sleep(60)
    print(f"Alerts are being fulfilled at {current_closest_minute()}")
    try: 
        serve_alert_client_2 =node_contract_0.fulfillAlert(alert_ID_client_2, {'from':mock_node_0,  "gas_price":"1 gwei"})
        served_alert_client_2 = Served_Alert_Tx(serve_alert_client_2, "client_main_second")
        test_balance = mock_node_1.balance()
        re_serve_alert_client_2 =node_contract_1.fulfillAlert(alert_ID_client_2, {'from':mock_node_1,  "gas_price":"1 gwei"})
        test_balance_01 = mock_node_1.balance()
        re_served_alert_client_2 = Served_Alert_Tx(re_serve_alert_client_2, "client_sec_second")
        serve_alert_benchmark_2 =node_contract_0.fulfillAlert(alert_ID_benchmark_2, {'from':mock_node_0,  "gas_price":"1 gwei"})
        served_alert_benchmark_2 = Served_Alert_Tx(serve_alert_benchmark_2, "benchmark_main_second")
        re_serve_alert_benchmark_2 =node_contract_1.fulfillAlert(alert_ID_benchmark_2, {'from':mock_node_1,  "gas_price":"1 gwei"})
        re_served_alert_benchmark_2 = Served_Alert_Tx(re_serve_alert_benchmark_2, "benchmark_sec_second")
    except Exception as e:
        print(e)
    result = {"First_Serving":[vars(served_alert_client_1),vars(re_served_alert_client_1),vars(served_alert_benchmark_1),vars(re_served_alert_benchmark_1)],"Second_Serving":[vars(served_alert_client_2),vars(re_served_alert_client_2),vars(served_alert_benchmark_2),vars(re_served_alert_benchmark_2)]}
    with open ('./references/gas_measures.json','w+') as f:
        json.dump(result, f)
    print(f"test balance = {test_balance, test_balance_01, re_serve_alert_client_2.gas_price} actual balance = {re_serve_alert_client_2.gas_used}")
    print(f"Trace of new protocol first served, total gas {serve_alert_client_1.gas_used} ")
    serve_alert_client_1.call_trace(True)
    print(f"Trace of new protocol second served, , total gas {re_serve_alert_client_1.gas_used} ")
    re_serve_alert_client_1.call_trace(True)
    print(f"Trace of re-used protocol first served, total gas {serve_alert_client_2.gas_used} ")
    serve_alert_client_2.call_trace(True)
    print(f"Trace of re-used protocol second served, , total gas {re_serve_alert_client_2.gas_used} ")
    re_serve_alert_client_2.call_trace(True)