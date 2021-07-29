// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "interfaces/KhronusCoordinatorInterface.sol";

abstract contract KhronusClient{

KhronusCoordinatorInterface private KhronusCoordinator;

address khronusCoordinator;
    
    constructor (address _khronusCoordinator){
        khronusCoordinator = _khronusCoordinator;
        KhronusCoordinator = KhronusCoordinatorInterface(_khronusCoordinator);
    }

    function requestKhronTab(uint256 _timeStamp, uint256 _iterations, string memory _khronTab) internal returns (bytes32){
        return KhronusCoordinator.requestKhronTab(_timeStamp, _iterations, _khronTab);
    }

    function khronProcess(bytes32 _requestID) internal virtual {
    }

    function khronResponse(bytes32 _requestID) external {
        require (msg.sender == khronusCoordinator);
        khronProcess(_requestID);
    }
}