// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface KhronClientInterface {
    function KhronTask_Integer(
        bytes memory requestID,
        bytes memory data,
        uint256  khronValue
    )
    external
    returns (bool);
    
    function KhronTask_Bytes(
        bytes memory requestID,
        bytes memory data,
        bytes memory khronValue
    )
    external
    returns (bool);

    function KhronTask_Bool(
        bytes memory requestID,
        bytes memory data,
        bytes memory khronValue
    )
    external
    returns (bool);

    function KhronTaks_Lever(
        bytes memory requestID,
        bytes memory data
    )
    external
    returns (bool);
}