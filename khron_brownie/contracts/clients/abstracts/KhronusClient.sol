// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "interfaces/token/KhronTokenInterface.sol";

abstract contract KhronusClient {

    KhronTokenInterface private khronus;

    function setKhronTokenAddress(
        address khronAddress
        )
        external
        {
            khronus = KhronTokenInterface(khronAddress);
        }

    function setKhronTab(
        address khronNode,
        uint256 khronFee,
        bytes memory data
        )
        external
        returns (bool)
        {
            return khronus.transferAndCall(khronNode,khronFee, data);
        }
}