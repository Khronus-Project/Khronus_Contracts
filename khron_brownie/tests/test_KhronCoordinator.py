import pytest
from brownie import Wei, accounts, TestKhronusCoordinator, InterestDeposit, KhronToken

@pytest.fixture
def tokenContract():
    return KhronToken.deploy({'from':accounts[0]})

@pytest.fixture
def coordinatorContract():
    return TestKhronusCoordinator.deploy({'from':accounts[0]})

@pytest.fixture
def clientContract():
    return InterestDeposit.deploy({'from':accounts[1]})



def test_clientRegistration(tokenContract,coordinatorContract,clientContract):
    coordinatorContract.setKhronTokenAddress(tokenContract.address,{'from':accounts[0]})
    clientOwnerBalance = tokenContract.balanceOf(accounts[1].address)
    clientContractBalance = coordinatorContract.creditOf(clientContract.address)
    tokenContract.transfer(accounts[1].address, 100*10**18,{'from':accounts[0]})
    clientOwnerBalance += 100*10**18
    tokenContract.increaseAllowance(coordinatorContract, 50*10**18, {'from':accounts[1]})
    coordinatorContract.fundClient(clientContract.address, 50*10**18, {'from':accounts[1]})
    assert tokenContract.balanceOf(clientContract.address) == clientOwnerBalance - 50*10**18
    assert coordinatorContract.creditOf(clientContract.address) == clientContractBalance + 50*10**18


#def test_clientSendRequest():
