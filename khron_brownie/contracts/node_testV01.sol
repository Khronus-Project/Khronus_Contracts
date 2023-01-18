// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

//Local Import from package source
//import "Khronus_Utils/contracts/KhronusNodeBaseV01.sol";
//Remote import from repo
import "@khronus/khronus-utils@0.0.4/contracts/KhronusNodeBaseV01.sol";


contract TestKhronusNode01 is KhronusNode {
    constructor (address _khronus_Coordinator) KhronusNode(_khronus_Coordinator) {
    }
}