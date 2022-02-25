import pytest
from datetime import datetime, timezone
from testing_utils import logger, khron_constants_node

@pytest.fixture
def constants():
    return khron_constants_node()

@pytest.fixture
def current_utc_timestamp():
    return int(datetime.now(timezone.utc).timestamp())

def test_register_node_happy_path(constants,current_utc_timestamp):
    # Set up constants for testing
    token_contract = constants["Token_Contract"]
    coordinator_contract = constants["Coordinator_Contract"]
    node_contract = constants["Node_Contracts"][0]
    node_owner = constants["Node_Owners"][0]
    # Test Body
    txt = coordinator_contract.registerNode(node_contract.address,{'from':node_owner})
    node_index = txt.return_value
    # Test Logs
    current_time = datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime()
    data = {'Test':'register_node','TestTime':current_time, 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Node":node_contract.address}, "Events":txt.events}
    logger(data)
    # Assertion
    assert coordinator_contract.getNodeFromIndex(node_index) == node_contract.address
    
def test_register_node_twice_error(constants,current_utc_timestamp):
    # Set up constants for testing
    token_contract = constants["Token_Contract"]
    coordinator_contract = constants["Coordinator_Contract"]
    node_contract = constants["Node_Contracts"][0]
    node_owner_0 = constants["Node_Owners"][0]
    node_owner_1 = constants["Node_Owners"][1]
    isValid = True
    # Test Body
    coordinator_contract.registerNode(node_contract.address,{'from':node_owner_0})
    current_time = datetime.fromtimestamp(current_utc_timestamp,timezone.utc).ctime()
    try:
        txt = coordinator_contract.registerNode(node_contract.address,{'from':node_owner_1})
        node_index = txt.return_value
        data = {'Test':'register_node','TestTime':current_time, 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Node":node_contract.address}, "Events":txt.events}
        logger(data)
        # Assertion
    except Exception as e:
        data = {'Test':'register_node','TestTime':current_time, 'TestingAddresses':{"Token":token_contract.address, "Coordinator":coordinator_contract.address,"Node":node_contract.address}, "Exception":e.message}
        value = e.message
        logger(e.message)
       
        # Assertion
    assert value == "VM Exception while processing transaction: revert Node is already registered"
    
    