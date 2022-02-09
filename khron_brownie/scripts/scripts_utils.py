from brownie import accounts, KhronusCoordinator, EscrowInfrastructure, KhronToken, TestKhronusNode, MockOracle, KhronPriceOracle
# Testing utilities

def khron_constants_client():
    # Constants
    total_client_tokens = 1000*10**18
    registration_deposit = 100*10**18
    tolerance_band = 5
    khron_owner = accounts[0]
    client_owner = accounts[1]
    token_contract = KhronToken.deploy({"from":khron_owner})
    eth_oracle = MockOracle.deploy(5000*1e8, {"from":accounts[0]})
    matic_oracle = MockOracle.deploy(2*1e8, {"from":accounts[0]})
    khron_oracle = KhronPriceOracle.deploy(eth_oracle.address, matic_oracle.address, {"from":accounts[0]})
    coordinator_contract = KhronusCoordinator.deploy(token_contract.address, khron_oracle.address, registration_deposit, tolerance_band,{'from':khron_owner})
    client_contract = EscrowInfrastructure.deploy(coordinator_contract.address,{"from":client_owner})
    token_contract.transfer(client_owner.address, total_client_tokens,{"from":khron_owner})
    client_constants = {"Token_Contract":token_contract,
                        "Coordinator_Contract":coordinator_contract, 
                        "Client_Contract":client_contract,
                        "Khron_Owner":khron_owner,
                        "Client_Owner":client_owner,
                        "Registration_Deposit":registration_deposit}
    return (client_constants)
    