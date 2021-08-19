
from brownie import accounts, KhronusCoordinator, EscrowInfrastructure, KhronToken, TestKhronusNode
# Testing utilities

def khron_constants_client():
    # Constants
    totalClientTokens = 100*10**18
    registrationDeposit = 1*10**18
    callPrice = 0.1*10**18
    khronOwner = accounts[0]
    clientOwner = accounts[1]
    tokenContract = KhronToken.deploy({'from':khronOwner})
    coordinatorContract = KhronusCoordinator.deploy(tokenContract.address, registrationDeposit, callPrice,{'from':khronOwner})
    clientContract = EscrowInfrastructure.deploy(coordinatorContract.address,{'from':clientOwner})
    tokenContract.transfer(clientOwner.address, totalClientTokens,{'from':khronOwner})
    return (tokenContract, coordinatorContract, clientContract, khronOwner, clientOwner)

def khron_constants_node():
    registrationDeposit = 1*10**18
    callPrice = 0.1*10**18
    khronOwner = accounts[0]
    nodeOwner_0 = accounts[4]
    nodeOwner_1 = accounts[5]
    tokenContract = KhronToken.deploy({'from':khronOwner})
    coordinatorContract = KhronusCoordinator.deploy(tokenContract.address, registrationDeposit, callPrice,{'from':khronOwner})
    nodeContract_0 = TestKhronusNode.deploy({'from':nodeOwner_0})
    nodeContract_1 = TestKhronusNode.deploy({'from':nodeOwner_1})
    return (tokenContract, coordinatorContract, nodeContract_0, nodeContract_1, khronOwner, nodeOwner_0, nodeOwner_1)

def khron_contants_operations():
    total_client_tokens = 100*10**18
    registration_deposit = 1*10**18
    call_price = 0.1*10**18
    khron_owner = accounts[0]
    client_owner = accounts[1]
    node_owner_0 = accounts[4]
    node_owner_1 = accounts[5]
    token_contract = KhronToken.deploy({'from':khron_owner})
    coordinator_contract = KhronusCoordinator.deploy(token_contract.address, registration_deposit, call_price,{'from':khron_owner})
    client_contract = EscrowInfrastructure.deploy(coordinator_contract.address,{'from':client_owner})
    node_contract_0 = TestKhronusNode.deploy({'from':node_owner_0})
    node_contract_1 = TestKhronusNode.deploy({'from':node_owner_1})
    token_contract.transfer(client_owner.address, total_client_tokens,{'from':khron_owner})
    coordinator_contract.registerNode(node_contract_0.address,{'from':node_owner_0})
    coordinator_contract.registerNode(node_contract_1.address,{'from':node_owner_1})
    token_contract.increaseApproval(coordinator_contract.address, registration_deposit, {'from':client_owner})
    coordinator_contract.registerClient(client_contract.address, registration_deposit, {'from':client_owner})
    return (token_contract, coordinator_contract, client_contract, node_contract_0, node_contract_1, khron_owner, client_owner, node_owner_0, node_owner_1, call_price)

def logger(data):
    buffer = str(data)
    with open ('./tests/logger.txt', 'a') as f:
        f.write(buffer+'\n')