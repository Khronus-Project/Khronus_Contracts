// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "interfaces/KhronusCoordinatorInterface.sol";
import "libraries/khronTimestampUtils.sol";


abstract contract KhronusClient{

KhronusCoordinatorInterface private KhronusCoordinator;
address owner;
address khronusCoordinator;
    
    constructor (address _khronusCoordinator){
        khronusCoordinator = _khronusCoordinator;
        KhronusCoordinator = KhronusCoordinatorInterface(_khronusCoordinator);
        owner = msg.sender;
    }

    function clientRequestKhronTab(uint256 _timestamp, uint256 _iterations, string memory _khronTab) internal returns (bytes32){
        require(KhronusTimeCog.isValidTimestamp(_timestamp), "the timestamp is not valid");
        uint256 _processedTimestamp = _processTimeStamp(_timestamp);
        return KhronusCoordinator.requestKhronTab(_processedTimestamp, _iterations, _khronTab);
    }

    function khronProcessAlert(bytes32 _requestID) internal virtual returns (bool) {
    }

    function khronResponse(bytes32 _requestID) external returns (bool){
        require (msg.sender == khronusCoordinator);
        khronProcessAlert(_requestID);
        return true;
    }


    // pending to emit an event here to record the change of coordinator
    function changeCoordinator(address _newCoordinator) external {
        require (msg.sender == owner, "only owner function");
        khronusCoordinator = _newCoordinator;
        KhronusCoordinator = KhronusCoordinatorInterface(_newCoordinator);
    }

    //internal logic functions for timestamp transformation
    function _processTimeStamp(uint256 _timestamp) internal view returns (uint256){
        uint256 _currentTimestamp = block.timestamp;
        require (KhronTimestampUtils.closestMinuteExact(_timestamp) > KhronTimestampUtils.closestMinuteExact(_currentTimestamp), "alerts are only allowed at least one minute in the future");
        return KhronTimestampUtils.closestMinuteExact(_timestamp);
    }
}