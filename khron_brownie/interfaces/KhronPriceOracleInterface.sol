// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface KhronPriceOracleInterface {
    function getLatestPriceKhronETH() 
        external 
        view 
        returns (uint);
}