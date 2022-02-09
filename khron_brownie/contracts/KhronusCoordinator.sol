// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "../interfaces/KhronTokenInterface.sol";
import "../interfaces/KhronusClientInterface.sol";
import "../interfaces/KhronPriceOracleInterface.sol";
import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/access/Ownable.sol";
import "@khronus/time-cog@1.0.2/contracts/src/KhronusTimeCog.sol";

contract KhronusCoordinator is Ownable{
    
    //initialize interfaces

    KhronTokenInterface private khronus;
    KhronusClientInterface private khronusClient;
    KhronPriceOracleInterface private khronOracle;

    // Events
    event ClientFunded(address indexed client, address indexed requester, uint256 amount);
    event ClientRegistered(address indexed client, address indexed requester, uint256 timestamp);
    event RequestProcessed(address indexed client, bytes32 requestID, bytes data);
    event AlertDispatched(bytes32 indexed requestID,bytes32 alertID, address[2] assignedNode, uint256 gasCost);
    event AlertFulfilled(bytes32 indexed requestID,  address indexed servingNode,bytes32 alertID, alertStatus status);  
    event AlertMistaken(address indexed servingNode,bytes32 alertID, uint256 expectedTimestamp, uint256 actualTimestamp);
    event WorkflowCompleted(uint gasCost, uint accountedGas, uint txGasPrice);
    event NodeRegistered(address indexed node, bytes32 index);

    
    // Flag variables

    enum TypeOfRequest{
        khronTab,
        powerKhron
    }
    enum alertStatus {
        notFulfilled,
        fulfilledOnce,
        fulfilledTwice
    }

    // Data Configuration Variables

    uint256 registrationDeposit; //miminum khron require for registering a contract
    uint256 initialRequestDeposit; // khron transmited as part of the deposit when setting a request
    uint256 bandOfTolerance; // amount of time in minutes in which a dispatched alert is considered valid after its original timestamp
    uint256 protocolGasConstant; // amount of gas that is protocol const for any given alert that is served
    
    // ## client registry
    struct clientContract {
        address owner;
        uint256 credit;
        uint256 nonce;
        uint256 standing;
    }

    mapping (address => clientContract) clientRegistry;

    // ## node registry

    uint256 public nodeCorrelative;
    uint256 nodeNonce;

    struct nodeContract {
        uint256 requestsReceived;
        uint256 requestsFulfilled;
        uint256 requestsFailed;
        uint256 balance;
        uint256 standing;
        bool registered;
    }

    mapping (address => nodeContract) nodeRegistry;
    mapping (bytes32 => address) nodeIndex;

    // ## Requests Alerts and Payment Registry

    struct khronRequest {
        address clientContract;
        uint256 iterations;
        bool completed;
        bool served;
    }

    mapping (bytes32 => khronRequest) requestRegistry;
    
    struct khronAlert {
        bytes32 requestID;
        uint256 timestamp;
        alertStatus status;
        address[2] servingNodes;
    }

    mapping (bytes32 => khronAlert) alertRegistry;

    // contract contructor
    constructor (address _khronAddress, address _khronOracle, uint256 _registrationDeposit, uint256 _bandOfTolerance) {
        khronus = KhronTokenInterface(_khronAddress);
        khronOracle = KhronPriceOracleInterface(_khronOracle);
        registrationDeposit = _registrationDeposit;
        bandOfTolerance = 1 minutes * _bandOfTolerance;
        protocolGasConstant = 26684;
    }

    // Business Logic Function Section

    /* Functions to set configurations
    */

    function setRegistrationDeposit(uint256 _registrationDeposit) external onlyOwner returns(bool){
        registrationDeposit = _registrationDeposit;
        return true;
    }

    function setBandOfTolerance(uint256 _bandOfTolerance) external onlyOwner returns(bool){
        bandOfTolerance = 1 minutes * _bandOfTolerance;
    }

    function setProtocolGasConstant(uint256 _protocolGasConstant) external onlyOwner returns(bool){
        protocolGasConstant = _protocolGasConstant;
    }

     /* Client registration
    */

    function registerClient(address _clientContract, uint256 _deposit) external returns (bool){
        require(_deposit >= registrationDeposit, "Need to deposit the minimum amount of Khron");
        address _owner = msg.sender;
        clientRegistry[_clientContract].owner = _owner;
        _fundClient(_owner, _clientContract, _deposit);
        emit ClientRegistered(_clientContract,_owner, block.timestamp);
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

    //set khron request
    function requestKhronTab(uint256 _timestamp, uint256 _iterations, string memory _khronTab) external returns(bytes32){
        address _requester = msg.sender;
        require (_isValidKhronTimestamp(_timestamp), "timestamp granularity should be on integer minutes your timestamp was not generated through the standard functionality on client contract or you overrode the function");
        address _owner = clientRegistry[_requester].owner;
        bytes32 _requestID = keccak256(abi.encodePacked(_requester, clientRegistry[_requester].nonce));
        clientRegistry[_requester].nonce += 1;
        requestRegistry[_requestID].iterations = _iterations;
        requestRegistry[_requestID].clientContract = _requester;
        if (_iterations <= 1){
            uint256 _iteration = 1;
            bytes memory _iterationsOrder = abi.encodePacked(_iteration,_iterations);
            _setKhronAlert(_requestID, _iterationsOrder, _timestamp);
        }
        else{
            //request calendar with the requestID
        }
        emit RequestProcessed(_requester, _requestID,abi.encode(_timestamp, _iterations, _khronTab));
        return _requestID;
    }

    /* Alerts Area
    /   1. Utilities for creating and serving alerts
    /   2. Set Individual Khron Alerts
    /   3. Set Khron Tabs
    /   4. Serve krhon alerts
    */
    
    //Alert utilities
    
    function _getServingNode() private returns (address){
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

    function _isAlertCorrect(bytes32 _alertID) private returns (bool){
        uint256 _current = block.timestamp;
        uint256 _target = alertRegistry[_alertID].timestamp;
        if (_current >= _target && _current <=_target + bandOfTolerance){
            return (true);
        }
        else{
            return (false);
        }
    }

    function _isValidKhronTimestamp(uint256 _timestamp) private pure returns (bool){
        if (_timestamp % 60 == 0 && KhronusTimeCog.isValidTimestamp(_timestamp)){
            return true;
        }
        else{
            return false;
        }
    }
    
    function _estimateKhron (bytes32 _alertID) private returns (uint) {

    }

    function _getKhronPrice() private returns (int){
        return khronOracle.getLatestPriceKhronETH();
    }

    //set khronAlerts
    function _setKhronAlert(bytes32 _requestID, bytes memory _alertOrder, uint256 _timestamp) private {
        uint _gasCost = gasleft(); // added just to evalute current gas cost of setting alerts
        bytes32 _alertID = keccak256(abi.encodePacked(_requestID, _alertOrder, _timestamp));
        alertRegistry[_alertID].requestID = _requestID;
        alertRegistry[_alertID].timestamp = _timestamp;
        string memory _eventTaskCode = '102'; //hardcoded CRUD event code 1 of task 02
        bytes memory _data = abi.encodePacked(_requestID, _alertID, _timestamp, _alertOrder, _eventTaskCode);
        for (uint256 _servingNodeI = 0; _servingNodeI < 2; _servingNodeI ++){
            address _servingNode = _getServingNode();
            alertRegistry[_alertID].servingNodes[_servingNodeI] = _servingNode;
            _dispatchToNodes(_servingNode, _data);
            nodeRegistry[_servingNode].requestsReceived += 1;
        }
        _gasCost -= gasleft(); // added just to evalute current gas cost of setting alerts
        emit AlertDispatched(_requestID, _alertID, alertRegistry[_alertID].servingNodes, _gasCost);
    }
    
    //serve khronAlerts 
    function serveKhronAlert(bytes32 _alertID) external returns (bool){
        uint gasCost = gasleft();
        uint _gasSpent;
        require(msg.sender == alertRegistry[_alertID].servingNodes[0] || msg.sender == alertRegistry[_alertID].servingNodes[1], "unauthorized Node cannot solve alert");
        address _servingNode = msg.sender;
        if (_isAlertCorrect(_alertID)) {
            nodeRegistry[_servingNode].requestsFulfilled += 1;
            address _clientContract = requestRegistry[alertRegistry[_alertID].requestID].clientContract;
            _gasSpent = gasCost - _processAlert(_alertID, _servingNode) + protocolGasConstant;
        }
        else {
           nodeRegistry[_servingNode].requestsFailed += 1;
           emit AlertMistaken(_servingNode, _alertID, alertRegistry[_alertID].timestamp, block.timestamp);
        }
        gasCost -= gasleft();
        emit WorkflowCompleted(gasCost, _gasSpent, tx.gasprice);
        return true;
    }

    function _processAlert(bytes32 _alertID, address _servingNode) private returns (uint) {
        bool _result;
        bytes32 _requestID = alertRegistry[_alertID].requestID;
        if (alertRegistry[_alertID].status == alertStatus.notFulfilled){
            KhronusClientInterface  _khronusClient;
            _khronusClient = KhronusClientInterface(requestRegistry[_requestID].clientContract);
            _result = _khronusClient.khronResponse(_requestID);
            _result ? alertRegistry[_alertID].status = alertStatus.fulfilledOnce: alertRegistry[_alertID].status = alertStatus.notFulfilled;
        }
        else{
            alertRegistry[_alertID].status = alertStatus.fulfilledTwice;
        }
        emit AlertFulfilled(_requestID, _servingNode, _alertID, alertRegistry[_alertID].status);
        return gasleft();
    }

    //set khronCalendars

    //View functions
    
    function getNodeFromIndex(bytes32 _index) external view returns(address){
        return nodeIndex[_index];
    }

    // check privacy of this function in non-development release
    function creditOf(address _clientContract) external view returns (uint256){
        return clientRegistry[_clientContract].credit;
    }

    // check privacy of this function in non-development release
    //function commitedFundsOf(address _clientContract) external view returns(uint256){
    //    return clientRegistry[_clientContract].commitedFunds;
    //}

    // check privacy of this function in non-development release
    function getAlertServers(bytes32 _alertID) external view returns(address[2] memory){
        return alertRegistry[_alertID].servingNodes;
    }

    // check privacy of this function in non-development release
    function getAlertRequest(bytes32 _alertID) external view returns(bytes32){
        return (alertRegistry[_alertID].requestID);
    }

    function getAlertTimestamp(bytes32 _alertID) external view returns(uint256){
        return (alertRegistry[_alertID].timestamp);
    }

    function getClientContract(bytes32 _requestID) external view returns(address){
        return (requestRegistry[_requestID].clientContract);
    }

    function getBandOfTolerance() external view returns (uint256){
        return bandOfTolerance;
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
        bytes memory _data
        )
        private
        returns (bool)
        {
            return khronus.transferAndCall(_nodeContract, initialRequestDeposit,_data);
        }
}