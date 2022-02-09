from brownie import accounts, KhronusCoordinator, EscrowInfrastructure, BasicClient, TestKhronusNode, KhronToken
import json
from time import sleep
from datetime import datetime, timezone

class Served_Alert_Tx:
    def __init__(self, served_alert_tx, transaction_label) -> None:
        self.transaction_label = transaction_label
        self.gas_used = served_alert_tx.gas_used
        self.gas_workflow_completed = served_alert_tx.events["WorkflowCompleted"]["gasCost"]
        self.gas_estimated = served_alert_tx.events["WorkflowCompleted"]["accountedGas"]
        self.delta_used_estimated = self.gas_used - self.gas_estimated
        self.estimation_correct = self.delta_used_estimated == 0

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
    with open ('../contract_library/contract_addresses_gas.json') as f:
        addresses = json.load(f)
    token_contract = KhronToken.at(addresses["KhronToken"])
    coordinator_contract = KhronusCoordinator.at(addresses["KhronusCoordinator"])
    client_contract = EscrowInfrastructure.at(addresses["KhronusClient"])
    benchmark_contract = BasicClient.at(addresses["KhronusBenchmark"])
    node_contract_0 = TestKhronusNode.at(addresses["KhronusNode_0"])
    node_contract_1 = TestKhronusNode.at(addresses["KhronusNode_1"])
    txt_request_client_1 = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {"from":escrow_depositor, "value":"1 ether"})
    txt_request_benchmark_1 = benchmark_contract.setTab(timestamp,{"from":escrow_depositor})
    alert_ID_client_1 = txt_request_client_1.events['AlertDispatched']['alertID']
    alert_ID_benchmark_1 = txt_request_benchmark_1.events['AlertDispatched']['alertID']
    sleep(60)
    print(f"Alerts are being fulfilled at {current_closest_minute()}")
    try: 
        serve_alert_client_1 =node_contract_0.fulfillAlert(alert_ID_client_1, {'from':mock_node_0})
        served_alert_client_1 = Served_Alert_Tx(serve_alert_client_1, "client_main_first")
        re_serve_alert_client_1 =node_contract_1.fulfillAlert(alert_ID_client_1, {'from':mock_node_1})
        re_served_alert_client_1 = Served_Alert_Tx(re_serve_alert_client_1, "client_sec_first")
        serve_alert_benchmark_1 =node_contract_0.fulfillAlert(alert_ID_benchmark_1, {'from':mock_node_0})
        served_alert_benchmark_1 = Served_Alert_Tx(serve_alert_benchmark_1, "benchmark_main_first")
        re_serve_alert_benchmark_1 =node_contract_1.fulfillAlert(alert_ID_benchmark_1, {'from':mock_node_1})
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
        serve_alert_client_2 =node_contract_0.fulfillAlert(alert_ID_client_2, {'from':mock_node_0})
        served_alert_client_2 = Served_Alert_Tx(serve_alert_client_2, "client_main_second")
        re_serve_alert_client_2 =node_contract_1.fulfillAlert(alert_ID_client_2, {'from':mock_node_1})
        re_served_alert_client_2 = Served_Alert_Tx(re_serve_alert_client_2, "client_sec_second")
        serve_alert_benchmark_2 =node_contract_0.fulfillAlert(alert_ID_benchmark_2, {'from':mock_node_0})
        served_alert_benchmark_2 = Served_Alert_Tx(serve_alert_benchmark_2, "benchmark_main_second")
        re_serve_alert_benchmark_2 =node_contract_1.fulfillAlert(alert_ID_benchmark_2, {'from':mock_node_1})
        re_served_alert_benchmark_2 = Served_Alert_Tx(re_serve_alert_benchmark_2, "benchmark_sec_second")
    except Exception as e:
        print(e)
    result = {"First_Serving":[vars(served_alert_client_1),vars(re_served_alert_client_1),vars(served_alert_benchmark_1),vars(re_served_alert_benchmark_1)],"Second_Serving":[vars(served_alert_client_2),vars(re_served_alert_client_2),vars(served_alert_benchmark_2),vars(re_served_alert_benchmark_2)]}
    with open ('../References/gas_measures.json','w') as f:
        json.dump(result, f)
    print(f"Trace of new protocol first served, total gas {serve_alert_client_1.gas_used} ")
    serve_alert_client_1.call_trace(True)
    print(f"Trace of new protocol second served, , total gas {re_serve_alert_client_1.gas_used} ")
    re_serve_alert_client_1.call_trace(True)
    print(f"Trace of re-used protocol first served, total gas {serve_alert_client_2.gas_used} ")
    serve_alert_client_2.call_trace(True)
    print(f"Trace of re-used protocol second served, , total gas {re_serve_alert_client_2.gas_used} ")
    re_serve_alert_client_2.call_trace(True)