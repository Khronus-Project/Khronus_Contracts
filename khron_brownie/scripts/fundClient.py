from brownie import Wei, accounts, KhronusCoordinator, InterestDeposit, KhronToken

def deployContract():
    tokenContract = KhronToken.deploy({'from':accounts[0]})
    coordinatorContract = KhronusCoordinator.deploy({'from':accounts[0]})
    clientContract = InterestDeposit.deploy({'from':accounts[1]})
    return (tokenContract, coordinatorContract, clientContract)

def main():
    deployContracts = deployContract()
    # Set up contracts for testing
    tokenContract = deployContracts[0]
    coordinatorContract = deployContracts[1]
    clientContract = deployContracts[2]
    coordinatorContract.setKhronTokenAddress(tokenContract.address,{'from':accounts[0]})
    # Setting initial variables
    totalClientTokens = 100*10**18
    clientCreditTokens = 50*10**18
    # Test Body
    clientOwnerBalance = tokenContract.balanceOf(accounts[1].address)
    clientOwnerAllowance = tokenContract.allowance(coordinatorContract.address, accounts[1].address)
    coordinatorBalance = tokenContract.balanceOf(coordinatorContract.address)
    clientContractBalance = coordinatorContract.creditOf(clientContract.address)
    tokenContract.transfer(accounts[1].address, totalClientTokens,{'from':accounts[0]})
    tokenContract.increaseApproval(coordinatorContract, clientCreditTokens, {'from':accounts[1]})
    print(coordinatorContract.fundClient.call(clientContract.address, clientCreditTokens, {'from':accounts[1]}))
    txt = coordinatorContract.fundClient(clientContract.address, clientCreditTokens, {'from':accounts[1]})
    print(tokenContract.balanceOf(accounts[1].address) == clientOwnerBalance + clientCreditTokens)
    print(tokenContract.balanceOf(coordinatorContract.address) == coordinatorBalance + clientCreditTokens)
    print(tokenContract.allowance(coordinatorContract.address, accounts[1].address) == clientOwnerAllowance + clientCreditTokens)
    print(coordinatorContract.creditOf(clientContract.address) == clientContractBalance + clientCreditTokens)
    print(txt.events)