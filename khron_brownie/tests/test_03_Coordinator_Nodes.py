from os import closerange
import pytest
from datetime import datetime
from testing_utils import logger, khron_constants_node

@pytest.fixture
def constants():
    return khron_constants_node()

def test_register_node(constants):
    # Set up constants for testing
    tokenContract = constants[0]
    coordinatorContract = constants[1]
    nodeContract = constants[2]
    nodeOwner = constants[4]
    # Test Body
    txt = coordinatorContract.registerNode(nodeContract.address,{'from':nodeOwner})
    nodeIndex = txt.return_value
    data = {'Test':'register_node','TestTime':datetime.utcnow().ctime(), 'TestingAddresses':{"Token":tokenContract.address, "Coordinator":coordinatorContract.address,"Client":nodeContract.address}, "Events":txt.events}
    logger(data)
    # Assertion
    assert coordinatorContract.getNodeFromIndex(nodeIndex) == nodeContract.address
    
