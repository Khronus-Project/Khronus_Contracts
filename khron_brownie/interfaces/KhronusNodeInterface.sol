// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface KhronusNodeInterface {
    function broadcast(address requester, bytes memory _data) external;
}