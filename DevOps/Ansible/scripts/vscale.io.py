#!/usr/bin/env python3

from os import environ, path, getenv
import requests
from dotenv import load_dotenv, find_dotenv
from json import loads, dumps
from time import time
from pprint import pprint
import argparse

load_dotenv(find_dotenv())
API_URL = "https://api.vscale.io/v1"


def do_request(
    url: str = f'{API_URL}/scalets',
    method: str = 'GET',
    payload: dict = '',
    headers: dict = {
        "Content-Type": "application/json;charset=UTF-8",
        "X-Token": f"{environ.get('VSCALE_IO_TOKEN')}"
    }
):
    result = requests.request(method, url, data=dumps(payload), headers=headers)
    return result.json()


def create_server(
    make_from: str = "ubuntu_16.04_64_001_master",
    rplan: str = "small",
    do_start: bool = True,
    name: str = '',
    keys: list = [],
    password: str = '',
    location: str = "spb0",
    count: int = 1
):
    """Create one server.

    make_from:
      # Id образа или бэкапа, на основе которого будет создан сервер
      - ubuntu_16.04_64_001_master
    
    rplan:
      # Установленный тарифный план
      small | medium | large | huge | monster
    
    do_start:
      # Нужно ли запускать сервер после создания
    """

    if not password:
        password = "Zxcdsaqwe321!@#"
    
    data = {
        "make_from": make_from,
        "rplan": rplan,
        "do_start": do_start,
        "password": password,
        "location": location
    }

    if keys:
        data["keys"] = keys
    
    if count:
        result = list()
        for _ in range(count):
            if not name:
                data["name"] = f"new-server-{time()}"
            result.append(do_request(method="POST", payload=data)["ctid"])
            del data["name"]
        return result
    else:
        if not name:
            data["name"] = f"new-server-{time()}"
        return do_request(method="POST", payload=data)["ctid"]


def server_list(ip_only: bool = False) -> list:
    """Show server list.
    """
    response = do_request()
    if ip_only:
        return [ip["public_address"]["address"] for ip in response]
    return response


def ssh_keys():
    """show SSH keys.
    """
    do_request(url="sshkeys")


def delete_server(server_id: int = '', all: bool = False):
    """Delete one server.
    """

    if all:
        for server in server_list():
            delete_server(server_id=server["ctid"])
    else: 
        do_request(
            method="DELETE",
            url=f"{API_URL}/scalets/{server_id}"
        )



if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(description="Vscale.io CLI mini-app.")

    

    # \ Main command \
    #  \ ------------ \
    arg_parser.add_argument("-v", "--verbose", help="Print debug texts.", action="store_true")

    # \ Sub-commands \
    #  \ ------------ \
    subparsers = arg_parser.add_subparsers(help='sub-commands for specific actions')

    # [>] Create sub-command
    create_parser = subparsers.add_parser("create", help="Create sub-command")

    #    - Create
    create_parser.add_argument("-s", "--server", help='string JSON data')

    # [>] Delete sub-command
    delete_parser = subparsers.add_parser("delete", help="delete sub-command")

    #    - Delete
    delete_parser.add_argument("-s", "--server", help="delete server", nargs="*")
    
    args = arg_parser.parse_args()
    print(args)
    

    # create_server(count=1)
    
    # print(
        # server_list(ip_only=True)
    # )
    
    # ssh_keys()
    
    # if args.delete:
    #     if args.delete == "all":
    #         delete_server(all=True)
    #     else:
    #         pass

    if 