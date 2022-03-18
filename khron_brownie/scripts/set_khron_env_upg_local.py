from brownie import accounts, TestKhronusNode, BasicClient, web3
from scripts.scripts_utils import khron_constants_proxy_setup
import json

def main():
    constants = khron_constants_proxy_setup()
    
    # Set up constants 
    
    token_contract = constants["Token_Contract"]
    coordinator_implementation = constants["Coordinator_Implementation"]
    coordinator_contract = constants["Coordinator_Contract"]
    client_contract = constants["Client_Contract"]
    client_owner = constants["Client_Owner"]
    benchmark_contract = BasicClient.deploy(coordinator_contract.address,{"from":client_owner})
    registration_deposit = constants["Registration_Deposit"]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    mock_node_0 = accounts[0]
    mock_node_1 = accounts[9]
    # Set environment 
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    call_register_client_0 = coordinator_implementation.registerClient.encode_input(client_contract.address, registration_deposit)
    web3.eth.send_transaction({"to":coordinator_contract.address,"from":client_owner.address,"data":call_register_client_0})
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    call_register_client_1 = coordinator_implementation.registerClient.encode_input(benchmark_contract.address, registration_deposit)
    web3.eth.send_transaction({"to":coordinator_contract.address,"from":client_owner.address,"data":call_register_client_1})
    node_contract_0 = TestKhronusNode.deploy(coordinator_contract.address,{'from':node_owner_0})
    node_contract_1 = TestKhronusNode.deploy(coordinator_contract.address,{'from':node_owner_1})
    node_contract_0.setKhronNode(mock_node_0.address,{'from':node_owner_0})
    node_contract_1.setKhronNode(mock_node_1.address,{'from':node_owner_1})
    call_register_node_0 = coordinator_implementation.registerNode.encode_input(node_contract_0.address)
    call_register_node_1 = coordinator_implementation.registerNode.encode_input(node_contract_1.address)
    web3.eth.send_transaction({"to":coordinator_contract.address,"from":node_owner_0.address,"data":call_register_node_0})
    web3.eth.send_transaction({"to":coordinator_contract.address,"from":node_owner_1.address,"data":call_register_node_1})
    # Record environment
    contracts = {"KhronToken": token_contract.address, "KhronusClient": client_contract.address, "KhronusBenchmark": benchmark_contract.address,"KhronusCoordinator":coordinator_contract.address,"KhronusOracle":constants["Khron_Oracle"].address, "KhronusNode_0": node_contract_0.address, "KhronusNode_1": node_contract_1.address}
    print(coordinator_contract.address)
    with open ('../contract_library/contract_addresses_proxied_local.json','w') as f:
       json.dump(contracts, f)