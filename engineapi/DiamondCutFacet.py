# Code generated by moonworm : https://github.com/bugout-dev/moonworm
# Moonworm version : 0.2.2

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from brownie import Contract, network, project
from brownie.network.contract import ContractContainer
from eth_typing.evm import ChecksumAddress


PROJECT_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BUILD_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "build", "contracts")


def boolean_argument_type(raw_value: str) -> bool:
    TRUE_VALUES = ["1", "t", "y", "true", "yes"]
    FALSE_VALUES = ["0", "f", "n", "false", "no"]

    if raw_value.lower() in TRUE_VALUES:
        return True
    elif raw_value.lower() in FALSE_VALUES:
        return False

    raise ValueError(
        f"Invalid boolean argument: {raw_value}. Value must be one of: {','.join(TRUE_VALUES + FALSE_VALUES)}"
    )


def bytes_argument_type(raw_value: str) -> str:
    return raw_value


def get_abi_json(abi_name: str) -> List[Dict[str, Any]]:
    abi_full_path = os.path.join(BUILD_DIRECTORY, f"{abi_name}.json")
    if not os.path.isfile(abi_full_path):
        raise IOError(
            f"File does not exist: {abi_full_path}. Maybe you have to compile the smart contracts?"
        )

    with open(abi_full_path, "r") as ifp:
        build = json.load(ifp)

    abi_json = build.get("abi")
    if abi_json is None:
        raise ValueError(f"Could not find ABI definition in: {abi_full_path}")

    return abi_json


def contract_from_build(abi_name: str) -> ContractContainer:
    # This is workaround because brownie currently doesn't support loading the same project multiple
    # times. This causes problems when using multiple contracts from the same project in the same
    # python project.
    PROJECT = project.main.Project("moonworm", Path(PROJECT_DIRECTORY))

    abi_full_path = os.path.join(BUILD_DIRECTORY, f"{abi_name}.json")
    if not os.path.isfile(abi_full_path):
        raise IOError(
            f"File does not exist: {abi_full_path}. Maybe you have to compile the smart contracts?"
        )

    with open(abi_full_path, "r") as ifp:
        build = json.load(ifp)

    return ContractContainer(PROJECT, build)


class DiamondCutFacet:
    def __init__(self, contract_address: Optional[ChecksumAddress]):
        self.contract_name = "DiamondCutFacet"
        self.address = contract_address
        self.contract = None
        self.abi = get_abi_json("DiamondCutFacet")
        if self.address is not None:
            self.contract: Optional[Contract] = Contract.from_abi(
                self.contract_name, self.address, self.abi
            )

    def deploy(self, transaction_config):
        contract_class = contract_from_build(self.contract_name)
        deployed_contract = contract_class.deploy(transaction_config)
        self.address = deployed_contract.address
        self.contract = deployed_contract
        return deployed_contract.tx

    def assert_contract_is_instantiated(self) -> None:
        if self.contract is None:
            raise Exception("contract has not been instantiated")

    def verify_contract(self):
        self.assert_contract_is_instantiated()
        contract_class = contract_from_build(self.contract_name)
        contract_class.publish_source(self.contract)

    def diamond_cut(
        self,
        _diamond_cut: List,
        _init: ChecksumAddress,
        _calldata: bytes,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.diamondCut(
            _diamond_cut, _init, _calldata, transaction_config
        )


def get_transaction_config(args: argparse.Namespace) -> Dict[str, Any]:
    signer = network.accounts.load(args.sender, args.password)
    transaction_config: Dict[str, Any] = {"from": signer}
    if args.gas_price is not None:
        transaction_config["gas_price"] = args.gas_price
    if args.max_fee_per_gas is not None:
        transaction_config["max_fee"] = args.max_fee_per_gas
    if args.max_priority_fee_per_gas is not None:
        transaction_config["priority_fee"] = args.max_priority_fee_per_gas
    if args.confirmations is not None:
        transaction_config["required_confs"] = args.confirmations
    if args.nonce is not None:
        transaction_config["nonce"] = args.nonce
    return transaction_config


def add_default_arguments(parser: argparse.ArgumentParser, transact: bool) -> None:
    parser.add_argument(
        "--network", required=True, help="Name of brownie network to connect to"
    )
    parser.add_argument(
        "--address", required=False, help="Address of deployed contract to connect to"
    )
    if not transact:
        parser.add_argument(
            "--block-number",
            required=False,
            type=int,
            help="Call at the given block number, defaults to latest",
        )
        return
    parser.add_argument(
        "--sender", required=True, help="Path to keystore file for transaction sender"
    )
    parser.add_argument(
        "--password",
        required=False,
        help="Password to keystore file (if you do not provide it, you will be prompted for it)",
    )
    parser.add_argument(
        "--gas-price", default=None, help="Gas price at which to submit transaction"
    )
    parser.add_argument(
        "--max-fee-per-gas",
        default=None,
        help="Max fee per gas for EIP1559 transactions",
    )
    parser.add_argument(
        "--max-priority-fee-per-gas",
        default=None,
        help="Max priority fee per gas for EIP1559 transactions",
    )
    parser.add_argument(
        "--confirmations",
        type=int,
        default=None,
        help="Number of confirmations to await before considering a transaction completed",
    )
    parser.add_argument(
        "--nonce", type=int, default=None, help="Nonce for the transaction (optional)"
    )
    parser.add_argument(
        "--value", default=None, help="Value of the transaction in wei(optional)"
    )
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")


def handle_deploy(args: argparse.Namespace) -> None:
    network.connect(args.network)
    transaction_config = get_transaction_config(args)
    contract = DiamondCutFacet(None)
    result = contract.deploy(transaction_config=transaction_config)
    print(result)
    print(result.info())


def handle_verify_contract(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = DiamondCutFacet(args.address)
    result = contract.verify_contract()
    print(result)


def handle_diamond_cut(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = DiamondCutFacet(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.diamond_cut(
        _diamond_cut=args.diamond_cut_arg,
        _init=args.init_arg,
        _calldata=args.calldata_arg,
        transaction_config=transaction_config,
    )
    print(result)
    if args.verbose:
        print(result.info())


def generate_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI for DiamondCutFacet")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers()

    deploy_parser = subcommands.add_parser("deploy")
    add_default_arguments(deploy_parser, True)
    deploy_parser.set_defaults(func=handle_deploy)

    verify_contract_parser = subcommands.add_parser("verify-contract")
    add_default_arguments(verify_contract_parser, False)
    verify_contract_parser.set_defaults(func=handle_verify_contract)

    diamond_cut_parser = subcommands.add_parser("diamond-cut")
    add_default_arguments(diamond_cut_parser, True)
    diamond_cut_parser.add_argument(
        "--diamond-cut-arg", required=True, help="Type: tuple[]", nargs="+"
    )
    diamond_cut_parser.add_argument("--init-arg", required=True, help="Type: address")
    diamond_cut_parser.add_argument(
        "--calldata-arg", required=True, help="Type: bytes", type=bytes_argument_type
    )
    diamond_cut_parser.set_defaults(func=handle_diamond_cut)

    return parser


def main() -> None:
    parser = generate_cli()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
