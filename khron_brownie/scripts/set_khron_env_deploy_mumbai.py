from brownie import accounts, KhronusCoordinatorV01, EscrowInfrastructure, TestKhronusNode01
import json
# Testing utilities

def khron_constants_client():
    # Constants
    protocol_owner = accounts.load("KhronTestMaster")
    client_owner = accounts.load("KhronTestClient")
    registration_deposit = 0.005*10**18
    tolerance_band = 5
    coordinator_contract = KhronusCoordinatorV01.deploy(registration_deposit, tolerance_band,{'from':protocol_owner})
    client_contract = EscrowInfrastructure.deploy(coordinator_contract.address,{"from":client_owner})
    client_constants = {"Coordinator_Contract":coordinator_contract, 
                        "Client_Contract":client_contract,
                        "Khron_Owner":protocol_owner,
                        "Client_Owner":client_owner,
                        "Registration_Deposit":registration_deposit}
    return (client_constants)

def main():
    constants = khron_constants_client()
    # Set up constants 
    coordinator_contract = constants["Coordinator_Contract"]
    client_contract = constants["Client_Contract"]
    client_owner = constants["Client_Owner"]
    node_owner_0 = accounts.load("KhronTestNode")
    registration_deposit = constants["Registration_Deposit"]
    # Set environment 
    coordinator_contract.registerClient(client_contract.address, {'from':client_owner, "value":registration_deposit})
    node_contract_0 = TestKhronusNode01.deploy(coordinator_contract.address,{'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    # Record environment
    contracts = {"KhronusClient": client_contract.address, "KhronusCoordinatorV01":coordinator_contract.address, "KhronusNode_0": node_contract_0.address}
    with open ('../contract_library/contract_addresses_deployment_bsc.json','w') as f:
        json.dump(contracts, f)