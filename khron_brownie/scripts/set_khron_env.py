from brownie import accounts, TestKhronusNode
from scripts.scripts_utils import khron_constants_client
import json

def main():
    constants = khron_constants_client()
    
    # Set up constants 
    
    token_contract = constants["Token_Contract"]
    coordinator_contract = constants["Coordinator_Contract"]
    client_contract = constants["Client_Contract"]
    client_owner = constants["Client_Owner"]
    registration_deposit = constants["Registration_Deposit"]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    
    # Set environment 
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    node_contract_0 = TestKhronusNode.deploy(coordinator_contract.address,{'from':node_owner_0})
    node_contract_1 = TestKhronusNode.deploy(coordinator_contract.address,{'from':node_owner_1})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_1.address,{'from':node_owner_1})
    # Record environment
    contracts = {"KhronToken": token_contract.address, "KhronusClient": client_contract.address, "KhronusCoordinator":coordinator_contract.address, "KhronusNode_0": node_contract_0.address, "KhronusNode_1": node_contract_1.address}
    with open ('../contract_library/contract_addresses.json','w') as f:
        json.dump(contracts, f)