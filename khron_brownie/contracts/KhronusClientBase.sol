// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "interfaces/KhronusCoordinatorInterface.sol";

abstract contract KhronusClient{

KhronusCoordinatorInterface private KhronusCoordinator;
address owner;
address khronusCoordinator;
    
    constructor (address _khronusCoordinator){
        khronusCoordinator = _khronusCoordinator;
        KhronusCoordinator = KhronusCoordinatorInterface(_khronusCoordinator);
        owner = msg.sender;
    }

    function _requestKhronTab(uint256 _timestamp, uint256 _iterations, string memory _khronTab) internal returns (bytes32){
        uint256 _processedTimestamp = _processTimeStamp(_timestamp);
        return KhronusCoordinator.requestKhronTab(_processedTimestamp, _iterations, _khronTab);
    }

    function khronProcessAlert(bytes32 _requestID) internal virtual returns (bool) {
    }

    function khronResponse(bytes32 _requestID) external {
        require (msg.sender == khronusCoordinator);
        khronProcessAlert(_requestID);
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
        require (_closestMinute(_timestamp) >= _closestMinute(_currentTimestamp), "cannot start alerts in the past");
        if (_closestMinute(_timestamp)==_closestMinute(_currentTimestamp)){
            return _closestMinute(_timestamp) + 60;
        }
        else{
            return _closestMinute(_timestamp);
        }
    }

    function _closestMinute(uint256 _timestamp) internal pure returns (uint256){
        uint256 _extraSeconds = _timestamp % 60;
        uint256 _interimAnswer = _timestamp - _extraSeconds;
        if (_extraSeconds < 30 ){
            return _interimAnswer;
        }
        else{
            return _interimAnswer +60;
        }
    }
}