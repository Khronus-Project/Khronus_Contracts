// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "contracts/KhronusClientBase.sol";

contract EscrowInfrastructure is KhronusClient{

    event EscrowCreated(address indexed depositor, bytes32 escrowID);

    struct escrow {
        uint256 deposit;
        uint256 expiryTimeStamp;
        address depositor;
        address beneficiary;
        bool condition;
        //bytes32 khronRequestId; //only for testing
    }

    uint256 nonce;

    mapping (bytes32 => escrow) private escrowRegistry; 
    mapping (bytes32 => bytes32) private tabRegistry;

    constructor(address _coordinatorAddress)
        public  
        KhronusClient(_coordinatorAddress){
    }

    function openEscrow(address _beneficiary, uint256 _expiryTimeStamp) external payable returns (bytes32){
        address _depositor = msg.sender;
        uint256 _deposit = msg.value; 
        bytes32 _escrowID = keccak256(abi.encodePacked(_depositor, nonce));
        escrowRegistry[_escrowID].deposit = _deposit;
        escrowRegistry[_escrowID].expiryTimeStamp = _expiryTimeStamp;
        escrowRegistry[_escrowID].depositor = _depositor;  
        escrowRegistry[_escrowID].beneficiary = _beneficiary;
        escrowRegistry[_escrowID].condition = false;
        bytes32 _requestID = requestKhronTab(_expiryTimeStamp, 1, "");
        tabRegistry[_requestID] = _escrowID;
        nonce += 1;
        emit EscrowCreated(_depositor, _escrowID);
        return _escrowID;
    }

    function khronFulfill(bytes32 _requestID) internal returns (bool){
        bytes32 _escrowID = tabRegistry[_requestID];
        if (escrowRegistry[_escrowID].condition == true){
            return true; //pending to implement transfer
        }
        else{
            return false; //pending to implement transfer
        }
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