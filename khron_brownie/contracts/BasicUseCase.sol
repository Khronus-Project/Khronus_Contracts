// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@khronus/khronus-client@0.0.4/contracts/KhronusClientBase.sol";

contract BasicClient is KhronusClient{

    event Requested(bytes32 requestID, uint timestamp);
    event Received(bytes32 requestID, uint timestamp);

    mapping (bytes32 => bool) private tabRegistry;

    constructor(address _coordinatorAddress)
        KhronusClient(_coordinatorAddress){
    }

    function setTab(uint256 _expiryTimestamp) external returns (bytes32){
        bytes32 _requestID = clientRequestKhronTab(_expiryTimestamp, 1, "");
        return _requestID;
        emit Requested(_requestID, block.timestamp);
    }
    
    function khronProcessAlert(bytes32 _requestID) override internal returns (bool){
        emit Received(_requestID, block.timestamp);
        return true;
    }
}