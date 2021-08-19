import pytest
from datetime import datetime
from testing_utils import logger, khron_constants_node

@pytest.fixture
def constants():
    return khron_constants_node()

def test_register_node_happy_path(constants):
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    nodeContract = constants[2]
    nodeOwner = constants[5]
    # Test Body
    txt = coordinatorContract.registerNode(nodeContract.address,{'from':nodeOwner})
    nodeIndex = txt.return_value
    data = {'Test':'register_node','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Node":nodeContract.address}, "Events":txt.events}
    logger(data)
    # Assertion
    assert coordinatorContract.getNodeFromIndex(nodeIndex) == nodeContract.address
    
def test_register_node_twice_error(constants):
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    nodeContract = constants[2]
    nodeOwner_0 = constants[4]
    nodeOwner_1 = constants[5]
    isValid = True
    # Test Body
    coordinatorContract.registerNode(nodeContract.address,{'from':nodeOwner_0})
    try:
        txt = coordinatorContract.registerNode(nodeContract.address,{'from':nodeOwner_1})
        nodeIndex = txt.return_value
        data = {'Test':'register_node','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Node":nodeContract.address}, "Events":txt.events}
        logger(data)
        # Assertion
    except Exception as e:
        data = {'Test':'register_node','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Node":nodeContract.address}, "Exception":e.message}
        logger(data)
        isValid = False
        # Assertion
    assert not isValid
    
    