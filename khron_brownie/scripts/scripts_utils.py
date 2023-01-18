from brownie import accounts, KhronusCoordinatorV01,  EscrowInfrastructure,  TestKhronusNode01, web3
# Testing utilities


class Served_Alert_Tx:
    def __init__(self, served_alert_tx, transaction_label) -> None:
        self.transaction_label = transaction_label
        self.gas_used = served_alert_tx.gas_used
        self.gas_workflow_completed = served_alert_tx.events["WorkflowCompleted"]["gasCost"]
        self.gas_estimated = served_alert_tx.events["WorkflowCompleted"]["accountedGas"]
        self.delta_used_estimated = self.gas_used - self.gas_estimated
        self.estimation_correct = self.delta_used_estimated == 0

def khron_constants_clientV01():
    # Constants
    registration_deposit = 0.5*10**18
    tolerance_band = 5
    khron_owner = accounts[0]
    client_owner = accounts[1]
    coordinator_contract = KhronusCoordinatorV01.deploy(registration_deposit, tolerance_band,{'from':khron_owner})
    client_contract = EscrowInfrastructure.deploy(coordinator_contract.address,{"from":client_owner})
    client_constants = {"Coordinator_Contract":coordinator_contract, 
                        "Client_Contract":client_contract,
                        "Khron_Owner":khron_owner,
                        "Client_Owner":client_owner,
                        "Registration_Deposit":registration_deposit}
    return (client_constants)
    

def khron_contants_operationsV01():
    registration_deposit = 1*10**18
    tolerance_band = 5
    khron_owner = accounts[0]
    client_owner = accounts[1]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    coordinator_contract = KhronusCoordinatorV01.deploy(registration_deposit, tolerance_band,{'from':khron_owner})
    client_contract = EscrowInfrastructure.deploy(coordinator_contract.address,{'from':client_owner})
    node_contract_0 = TestKhronusNode01.deploy(coordinator_contract.address, {'from':node_owner_0})
    node_contract_1 = TestKhronusNode01.deploy(coordinator_contract.address, {'from':node_owner_1})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_1.address,{'from':node_owner_1}) 
    coordinator_contract.registerClient(client_contract.address, {'from':client_owner, "value":registration_deposit})
    operations_constants = {
                            "Coordinator_Contract":coordinator_contract, 
                            "Client_Contract":client_contract,
                            "Node_Contracts":[node_contract_0, node_contract_0],
                            "Khron_Owner":khron_owner,
                            "Client_Owner":client_owner,
                            "Node_Operators":[node_owner_0,node_owner_1],
                            }
    return (operations_constants)

