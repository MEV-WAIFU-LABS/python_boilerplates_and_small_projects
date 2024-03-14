#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# author: Mia Stein

from utils.os import load_config, open_json, log_info
from utils.web3_wrapper import Web3Wrapper


def get_data_for_connection() -> dict:
    """Prepare a dict of data for connection."""

    data = {}
    env_keys = ['PAIR_ADDRESSES', 
                'PROVIDER_URL',
                'BLOCK_NUMBER',
                'ABI_JSON_PATH',
                'PROVIDER_TYPE']
    env_vars = load_config(env_keys) 

    data['addresses'] = env_vars['PAIR_ADDRESSES']
    data['network'] = env_vars['PROVIDER_URL']
    data['block'] = env_vars['BLOCK_NUMBER']
    data['abi'] = env_vars['ABI_JSON_PATH']
    data['provider_type'] = env_vars['PROVIDER_TYPE']  
    return data


def get_reserve_by_block(data) -> None:
    """Establish connection to retrieve reserve history."""

    w3 = Web3Wrapper(mode=data['provider_type'],
                     network=data['network'])
    w3.inject_middleware()    
    w3.get_pair_contract(data['addresses'], open_json(data['abi']))
    return w3.get_reserves(int(data['block']))
    

if __name__ == "__main__":

    data = get_data_for_connection()
    reserve1, reserve2 = get_reserve_by_block(data)
    log_info(f'reserves: {reserve1}, {reserve2}')
