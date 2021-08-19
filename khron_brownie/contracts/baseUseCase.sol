// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "contracts/KhronusClientBase.sol";

contract EscrowInfrastructure is KhronusClient{

    event EscrowCreated(address indexed depositor, bytes32 escrowID);
    event EscrowExpired(bytes32 indexed escrowID, uint256 timeStamp, bool conditionStatus);
    event ConditionChanged(bytes32 indexed escrowID, uint256 timeStamp, bool conditionStatus);

    enum EscrowStatus {Open, Expired}

    struct escrow {
        uint256 deposit;
        uint256 expiryTimeStamp;
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
        public  
        KhronusClient(_coordinatorAddress){
    }

    function openEscrow(address _beneficiary, uint256 _expiryTimeStamp, address _agent) external payable returns (bytes32){
        address _depositor = msg.sender;
        uint256 _deposit = msg.value; 
        bytes32 _escrowID = keccak256(abi.encodePacked(_depositor, nonce));
        escrowRegistry[_escrowID].deposit = _deposit;
        escrowRegistry[_escrowID].expiryTimeStamp = _expiryTimeStamp;
        escrowRegistry[_escrowID].depositor = _depositor;  
        escrowRegistry[_escrowID].beneficiary = _beneficiary;
        escrowRegistry[_escrowID].agent = _agent;
        escrowRegistry[_escrowID].condition = false;
        escrowRegistry[_escrowID].status = EscrowStatus.Open;
        bytes32 _requestID = _requestKhronTab(_expiryTimeStamp, 1, "");
        tabRegistry[_requestID] = _escrowID;
        nonce += 1;
        emit EscrowCreated(_depositor, _escrowID);
        return _escrowID;
    }

    function agentInput(bytes32 _escrowID, bool _conditionStatus) external {
        require (msg.sender == escrowRegistry[_escrowID].agent, "only agent can give input");
        escrowRegistry[_escrowID].condition = _conditionStatus;
        emit ConditionChanged(_escrowID, block.timestamp, _conditionStatus);
    }
    
    function khronProcessAlert(bytes32 _requestID) override internal returns (bool){
        bytes32 _escrowID = tabRegistry[_requestID];
        if (escrowRegistry[_escrowID].condition == true){
            payable(escrowRegistry[_escrowID].beneficiary).transfer(escrowRegistry[_escrowID].deposit);
            escrowRegistry[_escrowID].status = EscrowStatus.Expired;
            return true; //pending to implement transfer
        }
        else{
            payable(escrowRegistry[_escrowID].beneficiary).transfer(escrowRegistry[_escrowID].deposit);
            escrowRegistry[_escrowID].status = EscrowStatus.Expired;
            return false; //pending to implement transfer
        }
        emit EscrowExpired(_escrowID, block.timestamp, escrowRegistry[_escrowID].condition);
    }

    function seeDeposit(bytes32 _escrowID) external view returns(uint256) {
        return escrowRegistry[_escrowID].deposit;
    }

    function seeCondition(bytes32 _escrowID) external view returns(bool) {
        return escrowRegistry[_escrowID].condition;
    }

    function seeDepositor(bytes32 _escrowID) external view returns(address) {
        return escrowRegistry[_escrowID].depositor;
    }

    function seeBeneficiary(bytes32 _escrowID) external view returns(address) {
        return escrowRegistry[_escrowID].beneficiary;
    }

    function retrieveEscrowID(bytes32 _requestID) external view returns (bytes32) {
        return tabRegistry[_requestID];
    }
}