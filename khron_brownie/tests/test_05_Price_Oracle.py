import pytest
from brownie import KhronPriceOracle, MockOracle,accounts

def test_oracles():
    ethOracle = MockOracle.deploy(5000*1e8, {"from":accounts[0]})
    maticOracle = MockOracle.deploy(2*1e8, {"from":accounts[0]})
    khronOracle = KhronPriceOracle.deploy(ethOracle.address, maticOracle.address, {"from":accounts[0]})
    assert khronOracle.getLatestPriceKhronETH() == 0.0004 *1e18
