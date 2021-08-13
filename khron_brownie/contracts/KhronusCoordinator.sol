// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "interfaces/KhronTokenInterface.sol";
import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/access/Ownable.sol";

contract KhronusCoordinator is Ownable{
    //initialize interfaces

    KhronTokenInterface private khronus;
    
    // Events
    event ClientFunded(address indexed client, address indexed requester, uint256 amount);
    event RequestProcessed(address indexed client, bytes32 requestID, bytes data);
    event AlertDispatched(bytes32 indexed requestID,bytes32 alertID, address[2] assignedNodes);
    event NodeRegistered(address indexed node, bytes32 index);

    
    // Flag variables

    enum TypeOfRequest{
        khronTab,
        powerKhron
    }

    // # Data Variables

    uint256 callPrice;
    uint256 registrationDeposit;
    
    // ## client registry
    struct clientContract {
        address owner;
        uint256 credit;
        uint256 nonce;
        uint256 standing;
        uint256 commitedFunds;
    }

    mapping (address => clientContract) clientRegistry;

    // ## node registry

    uint256 public nodeCorrelative;
    uint256 public nodeNonce;

    struct nodeContract {
        uint256 requestsReceived;
        uint256 requestsResponded;
        uint256 requestFailed;
        uint256 standing;
        bool registered;
    }

    mapping (address => nodeContract) nodeRegistry;
    mapping (bytes32 => address) nodeIndex;

    // ## Requests and Alerts Registry

    struct khronRequest {
        uint256 iterations;
        bool completed;
        bool served;
    }

    mapping (bytes32 => khronRequest) requestRegistry;
    
    struct khronAlert {
        bytes32 requestID;
        uint256 timeStamp;
        bool served;
        address[2] servingNodes;
    }

    mapping (bytes32 => khronAlert) alertRegistry;

    // contract contructor
    constructor (address _khronAddress, uint256 _registrationDeposit,uint256 _callPrice) {
        khronus = KhronTokenInterface(_khronAddress);
        registrationDeposit = _registrationDeposit;
        callPrice = _callPrice;
    }

    // Business Logic Function Section

    /* Set Price Functions
    */

    function setCallPrice(uint256 _callPrice) external onlyOwner returns(bool){
        callPrice = _callPrice;
        return true;
    }

     function setRegistrationDeposit(uint256 _registrationDeposit) external onlyOwner returns(bool){
        registrationDeposit = _registrationDeposit;
        return true;
    }

     /* Client registration
    */

    function registerClient(address _clientContract, uint256 _deposit) external returns (bool){
        require(_deposit >= registrationDeposit, "Need to deposit the minimum amount of Khron");
        address _owner = msg.sender;
        clientRegistry[_clientContract].owner = _owner;
        _fundClient(_owner, _clientContract, _deposit);
    }
    
    function _fundClient(address _ownerAddress, address _clientContract, uint256 _deposit) internal{
        require (clientRegistry[_clientContract].owner == _ownerAddress, "only owner can fund");
        require (khronus.balanceOf(_ownerAddress) >= _deposit, "Not enough funds to transfer");
        require (khronus.allowance(_ownerAddress, address(this)) >= _deposit, "Not enough allowance to transfer funds");
        khronus.transferFrom(_ownerAddress, address(this), _deposit);
        clientRegistry[_clientContract].credit += _deposit;
        khronus.increaseApproval(_ownerAddress, _deposit);
        emit ClientFunded(_clientContract, _ownerAddress, _deposit);
    }
    
    function fundClient(address _clientContract, uint256 _deposit) external returns(bool){
        _fundClient(msg.sender, _clientContract, _deposit);
        return true;
    }

    /* Node registration functions
    */

    function registerNode(address _nodeAddress) external returns (bytes32){
        require (nodeRegistry[_nodeAddress].registered == false);
        bytes32 _index = keccak256(abi.encodePacked(nodeCorrelative,address(this)));
        nodeIndex[_index] = _nodeAddress;
        nodeCorrelative += 1;
        nodeRegistry[_nodeAddress].registered = true;
        emit NodeRegistered(_nodeAddress, _index);
        return _index;
    }   

    /* Request khronTab functions
    */

    //estimate cost
    function estimateKhron(TypeOfRequest _requestType, uint256 _iterations) internal returns(uint256){
        if (_requestType == TypeOfRequest.khronTab){
            if (_iterations <= 1) {
                return callPrice;
            }
            else{
                return callPrice * (_iterations+1);
            }
        }
    }

    //set khron request
    function requestKhronTab(uint256 _timeStamp, uint256 _iterations, string memory _khronTab) external returns(bytes32){
        uint256 _requestCost = estimateKhron(TypeOfRequest.khronTab, _iterations);
        address _requester = msg.sender;
        address _owner = clientRegistry[_requester].owner;
        require (clientRegistry[_requester].credit - clientRegistry[_requester].commitedFunds >= _requestCost, "Not enough funds in contract to set request");
        bytes32 _requestID = keccak256(abi.encodePacked(_requester, clientRegistry[_requester].nonce));
        clientRegistry[_requester].commitedFunds += _requestCost;
        khronus.decreaseApproval(_owner, _requestCost);
        clientRegistry[_requester].nonce += 1;
        requestRegistry[_requestID].iterations = _iterations;
        
        if (_iterations <= 1){
            uint256 _iteration = 1;
            bytes memory _iterationsOrder = abi.encodePacked(_iteration,_iterations);
            _setKhronAlert(_requestID, _iterationsOrder, _timeStamp);
        }
        else{
            //request calendar with the requestID
        }
        emit RequestProcessed(_requester, _requestID,abi.encode(_timeStamp, _iterations, _khronTab));
        return _requestID;
    }

    /* Alerts Area
    /   1. Utilities for creating the alerts
    /   2. Set Individual Khron Alerts
    /   3. Set Khron Tabs
    /   4. Solve krhon alerts
    */
    
    //Alert utilities
    
    function _getServingNode() internal returns (address){
        require (nodeCorrelative > 0, "No nodes available to serve requests");
        bytes32 _nodeIndex = keccak256(abi.encodePacked(nodeNonce,address(this)));
        if (nodeIndex[_nodeIndex] == address(0)){
            nodeNonce = 0;
            return _getServingNode();
        }
        else{
            address result = nodeIndex[_nodeIndex];
            nodeNonce += 1;
            return result;
        }
    }
        
    //set khronAlerts
    function _setKhronAlert(bytes32 _requestID, bytes memory _alertOrder, uint256 _timeStamp) internal {
        bytes32 _alertID = keccak256(abi.encodePacked(_requestID, _alertOrder, _timeStamp));
        alertRegistry[_alertID].requestID = _requestID;
        string memory _eventTaskCode = '102'; //hardcoded CRUD event code 1 of task 02
        bytes memory _data = abi.encodePacked(_requestID, _alertID, _timeStamp, _alertOrder, _eventTaskCode);
        uint256 _initialDeposit = (callPrice*5)/100;
        for (uint256 _servingNodeI = 0; _servingNodeI < 2; _servingNodeI ++){
            address _servingNode = _getServingNode();
            alertRegistry[_alertID].servingNodes[_servingNodeI] = _servingNode;
            _dispatchToNodes(_servingNode, _initialDeposit, _data);
            nodeRegistry[_servingNode].requestsReceived += 1;
        }
        emit AlertDispatched(_requestID, _alertID, alertRegistry[_alertID].servingNodes);
    }
    
    //set khronCalendars

    //View functions
    
    // check privacy of this function in non-development release
    function creditOf(address _clientContract) public view returns (uint256){
        return clientRegistry[_clientContract].credit;
    }

    function getCallPrice() public view returns (uint256){
        return callPrice;
    }

    // check privacy of this function in non-development release
    function commitedFundsOf(address _clientContract) public view returns(uint256){
        return clientRegistry[_clientContract].commitedFunds;
    }

    function getNodeFromIndex(bytes32 _index) public view returns(address){
        return nodeIndex[_index];
    }

    // check privacy of this function in non-development release
    function getAlertServers(bytes32 _alertID) public view returns(address[2] memory){
        return alertRegistry[_alertID].servingNodes;
    }

    //Request to node functions
    function setKhronTokenAddress(
        address _khronAddress
        )
        external
        onlyOwner
        returns (bool)
        {
            khronus = KhronTokenInterface(_khronAddress);
            return true;
        }


    function _dispatchToNodes(
        address _nodeContract, //this has to be a khron token recipient identifies the khron_node handling the request 
        uint256 _khronFee,
        bytes memory _data
        )
        internal
        returns (bool)
        {
            return khronus.transferAndCall(_nodeContract,_khronFee,_data);
        }
}