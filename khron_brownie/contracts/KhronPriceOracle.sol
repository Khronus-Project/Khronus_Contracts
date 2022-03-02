// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "interfaces/AggregatorV3Interface.sol";

contract KhronPriceOracle {

    AggregatorV3Interface internal priceEthUSDFeed;
    AggregatorV3Interface internal priceMaticUSDFeed;

    constructor(address _aggregatorEthUSD, address _aggregatorMaticUSD) {
        priceEthUSDFeed = AggregatorV3Interface(_aggregatorEthUSD);
        priceMaticUSDFeed = AggregatorV3Interface(_aggregatorMaticUSD);
    }

    /**
     * Returns the latest price of ETH
     */
    function _getLatestPriceEth() internal view returns (int) {
        (
            uint80 roundID, 
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceEthUSDFeed.latestRoundData();
        return price;
    }

    /**
     * Returns the latest price of ETH
     */
    function _getLatestPriceMatic() internal view returns (int) {
        (
            uint80 roundID, 
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceMaticUSDFeed.latestRoundData();
        return price;
    }

    function getLatestPriceKhronETH() external view returns (uint) {
        uint result;
        int priceEth = _getLatestPriceEth();
        int priceMatic = _getLatestPriceMatic();
        int price = (priceMatic * 1e18) /priceEth;
        price > 0 ? result = uint(price): result = 0;
        return result;
    }

}
