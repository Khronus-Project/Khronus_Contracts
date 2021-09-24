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
    escrowDepositor = accounts[2]
    escrowBeneficiary = accounts[3]
    agent = accounts[0]
    mockNode = accounts[0]
    timestamp = current_closest_minute() + 60
    with open ('../contract_library/contract_addresses.json') as f:
        addresses = json.load(f)
    TokenContract = KhronToken.at(addresses["KhronToken"])
    CoordinatorContract = KhronusCoordinator.at(addresses["KhronusCoordinator"])
    ClientContract = EscrowInfrastructure.at(addresses["KhronusClient"])
    NodeContract = TestKhronusNode.at(addresses["KhronusNode_0"])
    print(f"Initial balance of Node Contract is {TokenContract.balanceOf(NodeContract.address)/10**18}")
    txt_request = ClientContract.openEscrow(escrowBeneficiary, timestamp, agent, {"from":escrowDepositor, "value":"1 ether"})
    alert_ID = txt_request.events['AlertDispatched']['alertID']
    test_request = CoordinatorContract.getAlertRequest(alert_ID)
    print(f"Escrow ID is {txt_request.events['EscrowCreated']['escrowID']}")
    print(f"Initial status of Escrow is {ClientContract.getStatus(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"Initial balance of Escrow is {ClientContract.getBalance(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"Depositor of Escrow is {ClientContract.getDepositor(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"Beneficiary of Escrow is {ClientContract.getBeneficiary(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"Condition of Escrow is {ClientContract.getCondition(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"After creating escrow balance of Node Contract is {TokenContract.balanceOf(NodeContract.address)/10**18}")
    sleep(60)
    print(f"Alert was fulfilled at {current_closest_minute()}")
    try: 
        txt_serve = NodeContract.fulfillAlert(alert_ID, {'from':mockNode})
        print(txt_serve.events)
    except Exception as e:
        print(e.message)
    print(f"Status of Escrow after fulfillment is {ClientContract.getStatus(txt_request.events['EscrowCreated']['escrowID'])}")
    print(f"After creating correctly fulfilling the request balance of Node Contract is {TokenContract.balanceOf(NodeContract.address)/10**18}")
    print(test_request, alert_ID, txt_serve.return_value)