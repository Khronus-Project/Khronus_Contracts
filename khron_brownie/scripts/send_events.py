from brownie import accounts, TestKhronusCoordinator
import json

#Hex 'hello world' 68656c6c6f20776f726c64
#Hex 'this is real' 74686973206973207265616c

def main():
    message = '7b22526571756573744944223a2254455354524551554553543031222c2254797065223a223032222c22446566696e6974696f6e223a7b225374617274223a2231363235333130303030222c22454e44223a2231363235333137323030222c2243524f4e544142223a222a2f332a2a2a227d2c22414354494f4e53223a7b22494e5445524e414c223a7b225349474e4154555245223a2230783333633733316333222c22504152414d4554455253223a224e2f41222c224b48524f4e5f5441534b223a7b224e414d45223a224e2f41222c22504152414d4554455253223a224e2f41222c225349474e4154555245223a224e2f41227d7d7d7d0d0a'
    #message = '68656c6c6f20776f726c64'
    with open ('../contract_library/contract_addresses.json') as f:
        addresses = json.load(f)
    #with open ('build/contracts/KhronusCoordinator.json') as f:
    #    abiJson = json.load(f)
    tx = TestKhronusCoordinator.at(addresses['TestKhronusCoordinator']).setKhronTab(addresses['TestKhronusNode'],10**18,message,{'from':accounts[0]})
    data = []
    for log in tx.logs:
        dir = {}
        dir['address'] = log.address
        dir['topics'] = log.topics
        data.append(dir)        
    print (data)