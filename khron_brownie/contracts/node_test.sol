// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./KhronusNodeBase.sol";

contract TestKhronusNode is KhronusNode {
    constructor (address _khronus_Coordinator) KhronusNode(_khronus_Coordinator) {
        
    }
}