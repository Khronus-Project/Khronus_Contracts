from unittest import mock
from brownie import (
    accounts,
    Contract,
    #KhronusCoordinator, 
    KhronusCoordinatorV01,
    #KhronusCoordinatorImplementation,
    #TransparentUpgradeableProxy,
    #ProxyAdmin, 
    EscrowInfrastructure, 
    #KhronToken, 
    #TestKhronusNode,
    TestKhronusNode01, 
    #MockOracle, 
    #KhronPriceOracle,
    )
import json

# Testing utilities

def khron_constants_client01():
    # Constants
    registration_deposit = 0.5*10**18
    tolerance_band = 5
    khron_owner = accounts[0]
    client_owner = accounts[1]
    coordinator_contract = KhronusCoordinatorV01.deploy(registration_deposit, tolerance_band,{'from':khron_owner})
    client_contract = EscrowInfrastructure.deploy(coordinator_contract.address,{'from':client_owner})
    client_constants =  {   "Coordinator_Contract":coordinator_contract, 
                            "Client_Contract":client_contract,
                            "Khron_Owner":khron_owner,
                            "Client_Owner":client_owner,
                            "Registration_Deposit":registration_deposit
                            }
    return (client_constants)

def khron_constants_node():
    registration_deposit = 5*10**18
    tolerance_band = 5
    khron_owner = accounts[0]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    coordinator_contract = KhronusCoordinatorV01.deploy(registration_deposit, tolerance_band,{'from':khron_owner})
    node_contract_0 = TestKhronusNode01.deploy(coordinator_contract.address, {'from':node_owner_0})
    node_contract_1 = TestKhronusNode01.deploy(coordinator_contract.address, {'from':node_owner_1})
    node_constants={                    "Coordinator_Contract":coordinator_contract, 
                    "Node_Contracts":[node_contract_0, node_contract_1],
                    "Khron_Owner":khron_owner,
                    "Node_Owners":[node_owner_0,node_owner_1],
                    "Registration_Deposit":registration_deposit
                    }
    return (node_constants)





def logger(data):
    buffer = str(data)
    with open ('./tests/logger.txt', 'a') as f:
        f.write(buffer+'\n')

def khron_contants_operations01():
    registration_deposit = 0.5*10**18
    registration_deposit = 5*10**18
    tolerance_band = 5
    khron_owner = accounts[0]
    client_owner = accounts[1]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    mock_node_0 = accounts[9]
    mock_node_1 = accounts[8]
    gas_tolerance_fixed = 15000
    gas_tolerance_variable = 12
    gas_tolerance_total = gas_tolerance_fixed + gas_tolerance_variable
    coordinator_contract = KhronusCoordinatorV01.deploy(registration_deposit, tolerance_band,{'from':khron_owner})
    client_contract = EscrowInfrastructure.deploy(coordinator_contract.address,{'from':client_owner})
    node_contract_0 = TestKhronusNode01.deploy(coordinator_contract.address, {'from':node_owner_0})
    node_contract_1 = TestKhronusNode01.deploy(coordinator_contract.address, {'from':node_owner_1})
    node_contract_0.setKhronNode(mock_node_0.address,{'from':node_owner_0})
    node_contract_1.setKhronNode(mock_node_1.address,{'from':node_owner_1})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_1.address,{'from':node_owner_1})
    coordinator_contract.registerClient(client_contract.address, {'from':client_owner, "value":registration_deposit})
    operations_constants = {"Coordinator_Contract":coordinator_contract, 
                            "Client_Contract":client_contract,
                            "Node_Contracts":[node_contract_0, node_contract_1],
                            "Khron_Owner":khron_owner,
                            "Client_Owner":client_owner,
                            "Node_Operators":[node_owner_0,node_owner_1],
                            "Khron_Nodes":[mock_node_0,mock_node_1],
                            "Registration_Deposit":registration_deposit,
                            "Gas_Tolerance":gas_tolerance_total
                            }
    return (operations_constants)
