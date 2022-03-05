from brownie import accounts, KhronusCoordinator, KhronusCoordinatorImplementation, EscrowInfrastructure, KhronToken, TestKhronusNode, MockOracle, KhronPriceOracle
from scripts import set_khron_env_upg_local
import json

# Testing utilities

def khron_constants_client():
    # Constants
    total_client_tokens = 100*10**18
    registration_deposit = 5*10**18
    tolerance_band = 5
    khron_owner = accounts[0]
    client_owner = accounts[1]
    token_contract = KhronToken.deploy({'from':khron_owner})
    eth_oracle = MockOracle.deploy(5000*1e8, {"from":accounts[0]})
    matic_oracle = MockOracle.deploy(2*1e8, {"from":accounts[0]})
    khron_oracle = KhronPriceOracle.deploy(eth_oracle.address, matic_oracle.address, {"from":accounts[0]})
    coordinator_contract = KhronusCoordinator.deploy(token_contract.address, khron_oracle.address, registration_deposit, tolerance_band,{'from':khron_owner})
    client_contract = EscrowInfrastructure.deploy(coordinator_contract.address,{'from':client_owner})
    token_contract.transfer(client_owner.address, total_client_tokens,{'from':khron_owner})
    client_constants =  {"Token_Contract":token_contract,
                            "Coordinator_Contract":coordinator_contract, 
                            "Client_Contract":client_contract,
                            "Khron_Owner":khron_owner,
                            "Client_Owner":client_owner,
                            "Khron_Oracle":khron_oracle,
                            "Registration_Deposit":registration_deposit
                            }
    return (client_constants)

def khron_constants_node():
    registration_deposit = 5*10**18
    tolerance_band = 5
    khron_owner = accounts[0]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    token_contract = KhronToken.deploy({'from':khron_owner})
    eth_oracle = MockOracle.deploy(5000*1e8, {"from":accounts[0]})
    matic_oracle = MockOracle.deploy(2*1e8, {"from":accounts[0]})
    khron_oracle = KhronPriceOracle.deploy(eth_oracle.address, matic_oracle.address, {"from":accounts[0]}) 
    coordinator_contract = KhronusCoordinator.deploy(token_contract.address, khron_oracle.address, registration_deposit, tolerance_band,{'from':khron_owner})
    node_contract_0 = TestKhronusNode.deploy(coordinator_contract.address, {'from':node_owner_0})
    node_contract_1 = TestKhronusNode.deploy(coordinator_contract.address, {'from':node_owner_1})
    node_constants={"Token_Contract":token_contract,
                    "Coordinator_Contract":coordinator_contract, 
                    "Node_Contracts":[node_contract_0, node_contract_1],
                    "Khron_Owner":khron_owner,
                    "Node_Owners":[node_owner_0,node_owner_1],
                    "Registration_Deposit":registration_deposit
                    }
    return (node_constants)

def khron_contants_operations():
    total_client_tokens = 100*10**18
    registration_deposit = 5*10**18
    tolerance_band = 5
    khron_owner = accounts[0]
    client_owner = accounts[1]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    token_contract = KhronToken.deploy({'from':khron_owner})
    eth_oracle = MockOracle.deploy(5000*1e8, {"from":accounts[0]})
    matic_oracle = MockOracle.deploy(2*1e8, {"from":accounts[0]})
    khron_oracle = KhronPriceOracle.deploy(eth_oracle.address, matic_oracle.address, {"from":accounts[0]}) 
    coordinator_contract = KhronusCoordinator.deploy(token_contract.address, khron_oracle.address, registration_deposit, tolerance_band,{'from':khron_owner})
    client_contract = EscrowInfrastructure.deploy(coordinator_contract.address,{'from':client_owner})
    node_contract_0 = TestKhronusNode.deploy(coordinator_contract.address, {'from':node_owner_0})
    node_contract_1 = TestKhronusNode.deploy(coordinator_contract.address, {'from':node_owner_1})
    token_contract.transfer(client_owner.address, total_client_tokens,{'from':khron_owner})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_1.address,{'from':node_owner_1})
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    operations_constants = {"Token_Contract":token_contract,
                            "Coordinator_Contract":coordinator_contract, 
                            "Client_Contract":client_contract,
                            "Node_Contracts":[node_contract_0, node_contract_1],
                            "Khron_Owner":khron_owner,
                            "Client_Owner":client_owner,
                            "Node_Operators":[node_owner_0,node_owner_1],
                            "Khron_Oracle":khron_oracle,
                            "Registration_Deposit":registration_deposit
                            }
    return (operations_constants)


def khron_contants_operations_proxied():
    with open ('../contract_library/contract_addresses_proxied_local.json') as f:
        addresses = json.load(f)
    total_client_tokens = 100*10**18
    registration_deposit = 5*10**18
    khron_owner = accounts[0]
    client_owner = accounts[1]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    token_contract = KhronToken.at(addresses["KhronToken"])
    coordinator_contract = KhronusCoordinatorImplementation.at(addresses["KhronusCoordinator"])
    khron_oracle = KhronPriceOracle.at(addresses["KhronusOracle"])
    client_contract = EscrowInfrastructure.at(addresses["KhronusClient"])
    node_contract_0 = TestKhronusNode.at(addresses["KhronusNode_0"])
    node_contract_1 = TestKhronusNode.at(addresses["KhronusNode_1"])
    operations_constants = {"Token_Contract":token_contract,
                            "Coordinator_Contract":coordinator_contract, 
                            "Client_Contract":client_contract,
                            "Node_Contracts":[node_contract_0, node_contract_1],
                            "Khron_Owner":khron_owner,
                            "Client_Owner":client_owner,
                            "Node_Operators":[node_owner_0,node_owner_1],
                            "Khron_Oracle":khron_oracle,
                            "Registration_Deposit":registration_deposit
                            }
    return (operations_constants)

def set_env_upgradeable():
    set_khron_env_upg_local.main()

def logger(data):
    buffer = str(data)
    with open ('./tests/logger.txt', 'a') as f:
        f.write(buffer+'\n')
