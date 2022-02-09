from brownie import accounts, KhronusCoordinator, EscrowInfrastructure, TestKhronusNode, KhronToken
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
    with open ('../contract_library/contract_addresses.json') as f:
        addresses = json.load(f)
    token_contract = KhronToken.at(addresses["KhronToken"])
    coordinator_contract = KhronusCoordinator.at(addresses["KhronusCoordinator"])
    client_contract = EscrowInfrastructure.at(addresses["KhronusClient"])
    node_contract = TestKhronusNode.at(addresses["KhronusNode_0"])
    print(f"Initial balance of Node Contract is {token_contract.balanceOf(node_contract.address)/10**18}")
    txt_request = client_contract.openEscrow(escrow_beneficiary, timestamp, agent, {"from":escrow_depositor, "value":"1 ether"})
    alert_ID = txt_request.events['AlertDispatched']['alertID']
    test_request = coordinator_contract.getAlertRequest(alert_ID)
    print(f"Escrow ID is {txt_request.events['EscrowCreated']['escrowID']}")
    print(f"Initial status of Escrow is {client_contract.getStatus(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"Initial balance of Escrow is {client_contract.getBalance(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"Depositor of Escrow is {client_contract.getDepositor(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"Beneficiary of Escrow is {client_contract.getBeneficiary(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"Condition of Escrow is {client_contract.getCondition(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"After creating escrow balance of Node Contract is {token_contract.balanceOf(node_contract.address)/10**18}")
    sleep(60)
    print(f"Alert was fulfilled at {current_closest_minute()}")
    try: 
        txt_serve =node_contract.fulfillAlert(alert_ID, {'from':mock_node})
        print(f'Pure fulfillment cost is {txt_serve.events["AlertFulfilled"]["gasCost"]}')
        print(f'Workflow completed cost is {txt_serve.events["WorkflowCompleted"]["gasCost"]}')
        print(f'Estimated gas cost is {txt_serve.events["WorkflowCompleted"]["accountedGas"]}')
    except Exception as e:
        print(e.message)
    print(f"Status of Escrow after fulfillment is {client_contract.getStatus(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"After creating correctly fulfilling the request balance of Node Contract is {token_contract.balanceOf(node_contract.address)/10**18}")
    print(test_request, alert_ID, txt_serve.return_value)