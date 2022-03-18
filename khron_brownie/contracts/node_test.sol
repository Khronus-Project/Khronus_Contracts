// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

//Local Import from package source
//import "Khronus_Utils/contracts/KhronusNodeBase.sol";
//Remote import from repo
import "@khronus/khronus-utils@0.0.2/contracts/KhronusNodeBase.sol";


contract TestKhronusNode is KhronusNode {
    constructor (address _khronus_Coordinator) KhronusNode(_khronus_Coordinator) {
        
    }
}