// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

//Local Import from package source
//import "Khronus_Utils/contracts/KhronusClientBase.sol";

//remote import from package
import "@khronus/khronus-utils@0.0.3/contracts/KhronusClientBase.sol";

contract EscrowInfrastructure is KhronusClient{

    event EscrowCreated(address indexed depositor, bytes32 escrowID, uint256 timestamp, uint256 value);
    event EscrowExpired(bytes32 indexed escrowID, uint256 timeStamp, bool conditionStatus);
    event ConditionChanged(bytes32 indexed escrowID, uint256 timeStamp, bool conditionStatus);

    enum EscrowStatus {Open, Expired}

    struct escrow {
        uint256 balance;
        uint256 expiryTimestamp;
        address depositor;
        address beneficiary;
        address agent;
        bool condition;
        EscrowStatus status;
    }

    uint256 nonce;

    mapping (bytes32 => escrow) private escrowRegistry; 
    mapping (bytes32 => bytes32) private tabRegistry;

    constructor(address _coordinatorAddress)
        KhronusClient(_coordinatorAddress){
    }

    function openEscrow(address _beneficiary, uint256 _expiryTimestamp, address _agent) external payable returns (bytes32){
        address _depositor = msg.sender;
        uint256 _deposit = msg.value; 
        bytes32 _escrowID = keccak256(abi.encodePacked(_depositor, nonce));
        nonce += 1;
        escrowRegistry[_escrowID].balance = _deposit;
        escrowRegistry[_escrowID].expiryTimestamp = _expiryTimestamp;
        escrowRegistry[_escrowID].depositor = _depositor;  
        escrowRegistry[_escrowID].beneficiary = _beneficiary;
        escrowRegistry[_escrowID].agent = _agent;
        escrowRegistry[_escrowID].condition = false;
        escrowRegistry[_escrowID].status = EscrowStatus.Open;
        bytes32 _requestID = clientRequestKhronTab(_expiryTimestamp, 1, 0);
        tabRegistry[_requestID] = _escrowID;
        emit EscrowCreated(_depositor, _escrowID, _expiryTimestamp, _deposit);
        return _escrowID;
    }

    function agentInput(bytes32 _escrowID, bool _conditionStatus) external {
        require (msg.sender == escrowRegistry[_escrowID].agent, "only agent can give input");
        escrowRegistry[_escrowID].condition = _conditionStatus;
        emit ConditionChanged(_escrowID, block.timestamp, _conditionStatus);
    }
    
    function khronProcessAlert(bytes32 _requestID) override internal returns (bool){
        bytes32 _escrowID = tabRegistry[_requestID];
        if (escrowRegistry[_escrowID].condition){
            payable(escrowRegistry[_escrowID].beneficiary).transfer(escrowRegistry[_escrowID].balance);
            escrowRegistry[_escrowID].balance = 0;
            escrowRegistry[_escrowID].status = EscrowStatus.Expired;
        }
        else{
            payable(escrowRegistry[_escrowID].depositor).transfer(escrowRegistry[_escrowID].balance);
            escrowRegistry[_escrowID].balance = 0;
            escrowRegistry[_escrowID].status = EscrowStatus.Expired;
        }
        emit EscrowExpired(_escrowID, block.timestamp, escrowRegistry[_escrowID].condition);
        return true;
    }

    function getBalance(bytes32 _escrowID) external view returns(uint256) {
        return escrowRegistry[_escrowID].balance;
    }

    function getCondition(bytes32 _escrowID) external view returns(bool) {
        return escrowRegistry[_escrowID].condition;
    }

    function getDepositor(bytes32 _escrowID) external view returns(address) {
        return escrowRegistry[_escrowID].depositor;
    }

    function getBeneficiary(bytes32 _escrowID) external view returns(address) {
        return escrowRegistry[_escrowID].beneficiary;
    }

    function getEscrowID(bytes32 _requestID) external view returns (bytes32) {
        return tabRegistry[_requestID];
    }

    function getStatus(bytes32 _escrowID) external view returns (EscrowStatus) {
        return escrowRegistry[_escrowID].status;
    }

    function expiryManually(bytes32 _escrowID) external payable returns(bool) {
        require(block.timestamp >= escrowRegistry[_escrowID].expiryTimestamp,"require timestamp has passed to manually expire");
        if (escrowRegistry[_escrowID].condition){
            payable(escrowRegistry[_escrowID].beneficiary).transfer(escrowRegistry[_escrowID].balance);
            escrowRegistry[_escrowID].balance = 0;
            escrowRegistry[_escrowID].status = EscrowStatus.Expired;
        }
        else{
            payable(escrowRegistry[_escrowID].depositor).transfer(escrowRegistry[_escrowID].balance);
            escrowRegistry[_escrowID].balance = 0;
            escrowRegistry[_escrowID].status = EscrowStatus.Expired;
        }
        emit EscrowExpired(_escrowID, block.timestamp, escrowRegistry[_escrowID].condition);
        return true;
    }
}