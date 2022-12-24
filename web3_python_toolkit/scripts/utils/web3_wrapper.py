# -*- encoding: utf-8 -*-
# This class implements an (ongoing) wrapper for web3 libs.
# author: steinkirch

from web3 import Web3, HTTPProvider, WebsocketProvider, IPCProvider
from web3.middleware import geth_poa_middleware
from utils.os import log_info


class Web3Wrapper():

    def __init__(self, mode, network):
        self.mode = mode
        self.network = network

        self.w3 = None
        self.pair_contract = None

        self._setup()
    
    ##################
    # PRIVATE METHODS
    ##################
    def _setup(self) -> None:
        self._get_web3_object()

    def _get_web3_object(self) -> None:
        log_info(f'Setting mode {self.mode} for {self.network}')
        if self.mode == 'http' or self.mode == 'local_http':
            self.w3 = Web3(HTTPProvider(self.network))
        elif self.mode == 'ws' or self.mode == 'local_ws':
            self.w3 = Web3(WebsocketProvider(self.network))
        elif self.mode == 'ipc' or self.mode == 'local_ipc':
            self.w3 = Web3(IPCProvider(self.network))
        else:
            log_info(f'Provider type is invalid: {self.mode}. Fix .env.')


    ##################
    # BLOCK METHODS
    ##################
    def get_block(self, block_number='latest') -> dict:
        return dict(self.w3.eth.get_block(block_number))


    ##################
    # LP PAIR METHODS
    ##################
    def get_pair_contract(self, address, abi) -> str:
        self.pair_contract = self.w3.eth.contract(address=address, abi=abi)

    def inject_middleware(self, layer=0) -> None:
        self.w3.middleware_onion.inject(geth_poa_middleware, 
                                        layer=layer)
    
    def get_reserves(self, block) -> list:
        return self.pair_contract.functions.getReserves().call({}, block)[:2]


    ##############
    # TX METHODS
    ##############
    def get_tx(self, tx) -> dict:
        return dict(self.w3.eth.get_transaction(tx))

    def get_tx_receipt(self, tx) -> dict:
        return dict(self.w3.eth.get_transaction_receipt(tx))