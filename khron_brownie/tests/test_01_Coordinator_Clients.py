import pytest
from datetime import datetime, timezone
from testing_utils import logger, khron_constants_client01

@pytest.fixture
def constants01():
    return khron_constants_client01()

@pytest.fixture
def current_utc_timestamp():
    return int(datetime.now(timezone.utc).timestamp())

def test_register_client01(constants01, current_utc_timestamp):
    # Set up constants for testing
    coordinator_contract = constants01["Coordinator_Contract"]
    client_contract = constants01["Client_Contract"]
    client_owner = constants01["Client_Owner"]
    registration_deposit = constants01["Registration_Deposit"]
    # Test Body
    client_owner_balance = client_owner.balance()
    coordinator_balance = coordinator_contract.balance()
    client_contract_balance = coordinator_contract.getBalanceOf(client_contract.address)
    txt = coordinator_contract.registerClient(client_contract.address, {'from':client_owner, "value":registration_deposit})
    #Test Log
    current_time = datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime()
    data = {'Test':'registerClient','TestTime':current_time, 'TestingAddresses':{"Coordinator":coordinator_contract.address,"Client":client_contract.address}, "Events":dict(txt.events)}
    logger(data)
    # Assertion
    assert client_owner.balance() == client_owner_balance - registration_deposit
    assert coordinator_contract.balance() == coordinator_balance + registration_deposit
    assert coordinator_contract.getBalanceOf(client_contract.address) == client_contract_balance + registration_deposit

def test_fund_client01(constants01, current_utc_timestamp):
    # Set up constants for testing
    coordinator_contract = constants01["Coordinator_Contract"]
    client_contract = constants01["Client_Contract"]
    client_owner = constants01["Client_Owner"]
    registration_deposit = constants01["Registration_Deposit"]
    client_credit_tokens = 0.5*10**18
    coordinator_contract.registerClient(client_contract.address, {'from':client_owner, 'value':registration_deposit})
    # Test Body
    client_owner_balance = client_owner.balance()
    coordinator_balance = coordinator_contract.balance()
    client_contract_balance = coordinator_contract.getBalanceOf(client_contract.address)
    txt = coordinator_contract.fundClient(client_contract.address,  {'from':client_owner, 'value':client_credit_tokens})
    #Test Log
    current_time = datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime()
    data = {'Test':'fundClient','TestTime':current_time, 'TestingAddresses':{"Coordinator":coordinator_contract.address,"Client":client_contract.address}, "Events":dict(txt.events)}
    logger(data)
    # Assertion
    assert client_owner.balance() == client_owner_balance - client_credit_tokens
    assert coordinator_contract.balance() == coordinator_balance + client_credit_tokens
    assert coordinator_contract.getBalanceOf(client_contract.address) == client_contract_balance + client_credit_tokens