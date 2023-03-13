from brownie import accounts, KhronusCoordinatorV01, EscrowInfrastructure, TestKhronusNode01
import json
from time import sleep
from datetime import datetime, timezone

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
    mock_node = accounts[0]
    timestamp = current_closest_minute() + 60
    with open ('../contract_library/contract_addresses_local.json') as f:
        addresses = json.load(f)
    coordinator_contract = KhronusCoordinatorV01.at(addresses["KhronusCoordinator"])
    client_contract = EscrowInfrastructure.at(addresses["KhronusClient"])
    node_contract = TestKhronusNode01.at(addresses["KhronusNode_0"])
    txt_request = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {"from":escrow_depositor, "value":"1 ether"})
    alert_ID = txt_request.events['AlertDispatched']['alertID']
    print(f"Escrow ID is {txt_request.events['EscrowCreated']['escrowID']}")
    print(f"Initial status of Escrow is {client_contract.getStatus(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"Initial balance of Escrow is {client_contract.getBalance(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"Depositor of Escrow is {client_contract.getDepositor(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"Beneficiary of Escrow is {client_contract.getBeneficiary(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"Condition of Escrow is {client_contract.getCondition(txt_request.events['EscrowCreated']['escrowID'])}")
    sleep(60)
    print(f"Alert was fulfilled at {current_closest_minute()}")
    #try: 
    txt_serve = node_contract.fulfillAlert(alert_ID, {'from':mock_node})
    txt_serve.call_trace()
        #print(txt_serve.info)
        #print(f'Workflow completed cost is {txt_serve.events["WorkflowCompleted"]["gasCost"]}')
        #print(f'Estimated gas cost is {txt_serve.events["WorkflowCompleted"]["accountedGas"]}')
    #except Exception as e:
       #print(e.message)
    # print(f"Status of Escrow after fulfillment is {client_contract.getStatus(txt_request.events['EscrowCreated']['escrowID'])}")
    # print(test_request, alert_ID, txt_serve.return_value)