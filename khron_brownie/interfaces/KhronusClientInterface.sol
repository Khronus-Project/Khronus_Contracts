// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


interface KhronusClientInterface {
   
    // Interface Functions
    // Only owner and internal functions are not provided
    function khronResponse(bytes32 _requestID) external returns (bool);

}