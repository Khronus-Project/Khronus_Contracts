from brownie import accounts, TestKhronusNode01, BasicClient
from scripts.scripts_utils import khron_constants_clientV01
import json

def main():
    constants = khron_constants_clientV01()
    # Set up constants 
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
    coordinator_contract.registerClient(client_contract.address, {'from':client_owner, "value":registration_deposit})
    coordinator_contract.registerClient(benchmark_contract.address, {'from':client_owner, "value":registration_deposit})
    node_contract_0 = TestKhronusNode01.deploy(coordinator_contract.address,{'from':node_owner_0})
    node_contract_1 = TestKhronusNode01.deploy(coordinator_contract.address,{'from':node_owner_1})
    node_contract_0.setKhronNode(mock_node_0.address,{'from':node_owner_0})
    node_contract_1.setKhronNode(mock_node_1.address,{'from':node_owner_1})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_1.address,{'from':node_owner_1})
    # Record environment
    contracts = {"KhronusClient": client_contract.address, "KhronusBenchmark": benchmark_contract.address,"KhronusCoordinator":coordinator_contract.address, "KhronusNode_0": node_contract_0.address, "KhronusNode_1": node_contract_1.address}
    with open ('../contract_library/contract_addresses_local.json','w') as f:
        json.dump(contracts, f)