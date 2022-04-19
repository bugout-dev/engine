# Code generated by moonworm : https://github.com/bugout-dev/moonworm
# Moonworm version : 0.1.18

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


class Dropper:
    def __init__(self, contract_address: Optional[ChecksumAddress]):
        self.contract_name = "Dropper"
        self.address = contract_address
        self.contract = None
        self.abi = get_abi_json("Dropper")
        if self.address is not None:
            self.contract: Optional[Contract] = Contract.from_abi(
                self.contract_name, self.address, self.abi
            )

    def deploy(self, transaction_config):
        contract_class = contract_from_build(self.contract_name)
        deployed_contract = contract_class.deploy(transaction_config)
        self.address = deployed_contract.address
        self.contract = deployed_contract

    def assert_contract_is_instantiated(self) -> None:
        if self.contract is None:
            raise Exception("contract has not been instantiated")

    def verify_contract(self):
        self.assert_contract_is_instantiated()
        contract_class = contract_from_build(self.contract_name)
        contract_class.publish_source(self.contract)

    def erc1155_type(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.ERC1155_TYPE.call()

    def erc20_type(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.ERC20_TYPE.call()

    def erc721_type(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.ERC721_TYPE.call()

    def administrator_pool_id(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.administratorPoolId.call()

    def batch_claim(
        self,
        claim_ids: List,
        block_deadlines: List,
        amounts: List,
        signatures: List,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.batchClaim(
            claim_ids, block_deadlines, amounts, signatures, transaction_config
        )

    def claim(
        self,
        claim_id: int,
        block_deadline: int,
        quantity: int,
        signature: bytes,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.claim(
            claim_id, block_deadline, quantity, signature, transaction_config
        )

    def claim_message_hash(
        self,
        claim_id: int,
        claimant: ChecksumAddress,
        block_deadline: int,
        quantity: int,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.claimMessageHash.call(
            claim_id, claimant, block_deadline, quantity
        )

    def claim_status(self, claim_id: int) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.claimStatus.call(claim_id)

    def create_claim(
        self,
        token_type: int,
        token_address: ChecksumAddress,
        token_id: int,
        amount: int,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.createClaim(
            token_type, token_address, token_id, amount, transaction_config
        )

    def get_claim(self, claim_id: int) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.getClaim.call(claim_id)

    def get_claimed_amount_of_claiment(
        self, claim_id: int, claimant: ChecksumAddress
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.getClaimedAmountOfClaiment.call(claim_id, claimant)

    def get_signer_for_claim(self, claim_id: int) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.getSignerForClaim.call(claim_id)

    def num_claims(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.numClaims.call()

    def on_erc1155_batch_received(
        self,
        arg1: ChecksumAddress,
        arg2: ChecksumAddress,
        arg3: List,
        arg4: List,
        arg5: bytes,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.onERC1155BatchReceived(
            arg1, arg2, arg3, arg4, arg5, transaction_config
        )

    def on_erc1155_received(
        self,
        arg1: ChecksumAddress,
        arg2: ChecksumAddress,
        arg3: int,
        arg4: int,
        arg5: bytes,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.onERC1155Received(
            arg1, arg2, arg3, arg4, arg5, transaction_config
        )

    def on_erc721_received(
        self,
        operator: ChecksumAddress,
        from_: ChecksumAddress,
        token_id: int,
        data: bytes,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.onERC721Received(
            operator, from_, token_id, data, transaction_config
        )

    def owner(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.owner.call()

    def paused(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.paused.call()

    def renounce_ownership(self, transaction_config) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.renounceOwnership(transaction_config)

    def set_claim_status(self, claim_id: int, status: bool, transaction_config) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.setClaimStatus(claim_id, status, transaction_config)

    def set_signer_for_claim(
        self, claim_id: int, signer: ChecksumAddress, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.setSignerForClaim(claim_id, signer, transaction_config)

    def supports_interface(self, interface_id: bytes) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.supportsInterface.call(interface_id)

    def terminus_address(self) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.terminusAddress.call()

    def transfer_ownership(self, new_owner: ChecksumAddress, transaction_config) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.transferOwnership(new_owner, transaction_config)

    def withdraw_erc1155(
        self,
        token_address: ChecksumAddress,
        token_id: int,
        amount: int,
        transaction_config,
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.withdrawERC1155(
            token_address, token_id, amount, transaction_config
        )

    def withdraw_erc20(
        self, token_address: ChecksumAddress, amount: int, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.withdrawERC20(token_address, amount, transaction_config)

    def withdraw_erc721(
        self, token_address: ChecksumAddress, token_id: int, transaction_config
    ) -> Any:
        self.assert_contract_is_instantiated()
        return self.contract.withdrawERC721(token_address, token_id, transaction_config)


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


def handle_deploy(args: argparse.Namespace) -> None:
    network.connect(args.network)
    transaction_config = get_transaction_config(args)
    contract = Dropper(None)
    result = contract.deploy(transaction_config=transaction_config)
    print(result)


def handle_verify_contract(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.verify_contract()
    print(result)


def handle_erc1155_type(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.erc1155_type()
    print(result)


def handle_erc20_type(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.erc20_type()
    print(result)


def handle_erc721_type(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.erc721_type()
    print(result)


def handle_administrator_pool_id(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.administrator_pool_id()
    print(result)


def handle_batch_claim(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.batch_claim(
        claim_ids=args.claim_ids,
        block_deadlines=args.block_deadlines,
        amounts=args.amounts,
        signatures=args.signatures,
        transaction_config=transaction_config,
    )
    print(result)


def handle_claim(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.claim(
        claim_id=args.claim_id,
        block_deadline=args.block_deadline,
        quantity=args.quantity,
        signature=args.signature,
        transaction_config=transaction_config,
    )
    print(result)


def handle_claim_message_hash(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.claim_message_hash(
        claim_id=args.claim_id,
        claimant=args.claimant,
        block_deadline=args.block_deadline,
        quantity=args.quantity,
    )
    print(result)


def handle_claim_status(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.claim_status(claim_id=args.claim_id)
    print(result)


def handle_create_claim(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.create_claim(
        token_type=args.token_type,
        token_address=args.token_address,
        token_id=args.token_id,
        amount=args.amount,
        transaction_config=transaction_config,
    )
    print(result)


def handle_get_claim(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.get_claim(claim_id=args.claim_id)
    print(result)


def handle_get_claimed_amount_of_claiment(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.get_claimed_amount_of_claiment(
        claim_id=args.claim_id, claimant=args.claimant
    )
    print(result)


def handle_get_signer_for_claim(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.get_signer_for_claim(claim_id=args.claim_id)
    print(result)


def handle_num_claims(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.num_claims()
    print(result)


def handle_on_erc1155_batch_received(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.on_erc1155_batch_received(
        arg1=args.arg1,
        arg2=args.arg2,
        arg3=args.arg3,
        arg4=args.arg4,
        arg5=args.arg5,
        transaction_config=transaction_config,
    )
    print(result)


def handle_on_erc1155_received(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.on_erc1155_received(
        arg1=args.arg1,
        arg2=args.arg2,
        arg3=args.arg3,
        arg4=args.arg4,
        arg5=args.arg5,
        transaction_config=transaction_config,
    )
    print(result)


def handle_on_erc721_received(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.on_erc721_received(
        operator=args.operator,
        from_=args.from_arg,
        token_id=args.token_id,
        data=args.data,
        transaction_config=transaction_config,
    )
    print(result)


def handle_owner(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.owner()
    print(result)


def handle_paused(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.paused()
    print(result)


def handle_renounce_ownership(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.renounce_ownership(transaction_config=transaction_config)
    print(result)


def handle_set_claim_status(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.set_claim_status(
        claim_id=args.claim_id,
        status=args.status,
        transaction_config=transaction_config,
    )
    print(result)


def handle_set_signer_for_claim(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.set_signer_for_claim(
        claim_id=args.claim_id,
        signer=args.signer_arg,
        transaction_config=transaction_config,
    )
    print(result)


def handle_supports_interface(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.supports_interface(interface_id=args.interface_id)
    print(result)


def handle_terminus_address(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    result = contract.terminus_address()
    print(result)


def handle_transfer_ownership(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.transfer_ownership(
        new_owner=args.new_owner, transaction_config=transaction_config
    )
    print(result)


def handle_withdraw_erc1155(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.withdraw_erc1155(
        token_address=args.token_address,
        token_id=args.token_id,
        amount=args.amount,
        transaction_config=transaction_config,
    )
    print(result)


def handle_withdraw_erc20(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.withdraw_erc20(
        token_address=args.token_address,
        amount=args.amount,
        transaction_config=transaction_config,
    )
    print(result)


def handle_withdraw_erc721(args: argparse.Namespace) -> None:
    network.connect(args.network)
    contract = Dropper(args.address)
    transaction_config = get_transaction_config(args)
    result = contract.withdraw_erc721(
        token_address=args.token_address,
        token_id=args.token_id,
        transaction_config=transaction_config,
    )
    print(result)


def generate_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI for Dropper")
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers()

    deploy_parser = subcommands.add_parser("deploy")
    add_default_arguments(deploy_parser, True)
    deploy_parser.set_defaults(func=handle_deploy)

    verify_contract_parser = subcommands.add_parser("verify-contract")
    add_default_arguments(verify_contract_parser, False)
    verify_contract_parser.set_defaults(func=handle_verify_contract)

    erc1155_type_parser = subcommands.add_parser("erc1155-type")
    add_default_arguments(erc1155_type_parser, False)
    erc1155_type_parser.set_defaults(func=handle_erc1155_type)

    erc20_type_parser = subcommands.add_parser("erc20-type")
    add_default_arguments(erc20_type_parser, False)
    erc20_type_parser.set_defaults(func=handle_erc20_type)

    erc721_type_parser = subcommands.add_parser("erc721-type")
    add_default_arguments(erc721_type_parser, False)
    erc721_type_parser.set_defaults(func=handle_erc721_type)

    administrator_pool_id_parser = subcommands.add_parser("administrator-pool-id")
    add_default_arguments(administrator_pool_id_parser, False)
    administrator_pool_id_parser.set_defaults(func=handle_administrator_pool_id)

    batch_claim_parser = subcommands.add_parser("batch-claim")
    add_default_arguments(batch_claim_parser, True)
    batch_claim_parser.add_argument(
        "--claim-ids", required=True, help="Type: uint256[]", nargs="+"
    )
    batch_claim_parser.add_argument(
        "--block-deadlines", required=True, help="Type: uint256[]", nargs="+"
    )
    batch_claim_parser.add_argument(
        "--amounts", required=True, help="Type: uint256[]", nargs="+"
    )
    batch_claim_parser.add_argument(
        "--signatures", required=True, help="Type: bytes[]", nargs="+"
    )
    batch_claim_parser.set_defaults(func=handle_batch_claim)

    claim_parser = subcommands.add_parser("claim")
    add_default_arguments(claim_parser, True)
    claim_parser.add_argument(
        "--claim-id", required=True, help="Type: uint256", type=int
    )
    claim_parser.add_argument(
        "--block-deadline", required=True, help="Type: uint256", type=int
    )
    claim_parser.add_argument(
        "--quantity", required=True, help="Type: uint256", type=int
    )
    claim_parser.add_argument(
        "--signature", required=True, help="Type: bytes", type=bytes_argument_type
    )
    claim_parser.set_defaults(func=handle_claim)

    claim_message_hash_parser = subcommands.add_parser("claim-message-hash")
    add_default_arguments(claim_message_hash_parser, False)
    claim_message_hash_parser.add_argument(
        "--claim-id", required=True, help="Type: uint256", type=int
    )
    claim_message_hash_parser.add_argument(
        "--claimant", required=True, help="Type: address"
    )
    claim_message_hash_parser.add_argument(
        "--block-deadline", required=True, help="Type: uint256", type=int
    )
    claim_message_hash_parser.add_argument(
        "--quantity", required=True, help="Type: uint256", type=int
    )
    claim_message_hash_parser.set_defaults(func=handle_claim_message_hash)

    claim_status_parser = subcommands.add_parser("claim-status")
    add_default_arguments(claim_status_parser, False)
    claim_status_parser.add_argument(
        "--claim-id", required=True, help="Type: uint256", type=int
    )
    claim_status_parser.set_defaults(func=handle_claim_status)

    create_claim_parser = subcommands.add_parser("create-claim")
    add_default_arguments(create_claim_parser, True)
    create_claim_parser.add_argument(
        "--token-type", required=True, help="Type: uint256", type=int
    )
    create_claim_parser.add_argument(
        "--token-address", required=True, help="Type: address"
    )
    create_claim_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    create_claim_parser.add_argument(
        "--amount", required=True, help="Type: uint256", type=int
    )
    create_claim_parser.set_defaults(func=handle_create_claim)

    get_claim_parser = subcommands.add_parser("get-claim")
    add_default_arguments(get_claim_parser, False)
    get_claim_parser.add_argument(
        "--claim-id", required=True, help="Type: uint256", type=int
    )
    get_claim_parser.set_defaults(func=handle_get_claim)

    get_claimed_amount_of_claiment_parser = subcommands.add_parser(
        "get-claimed-amount-of-claiment"
    )
    add_default_arguments(get_claimed_amount_of_claiment_parser, False)
    get_claimed_amount_of_claiment_parser.add_argument(
        "--claim-id", required=True, help="Type: uint256", type=int
    )
    get_claimed_amount_of_claiment_parser.add_argument(
        "--claimant", required=True, help="Type: address"
    )
    get_claimed_amount_of_claiment_parser.set_defaults(
        func=handle_get_claimed_amount_of_claiment
    )

    get_signer_for_claim_parser = subcommands.add_parser("get-signer-for-claim")
    add_default_arguments(get_signer_for_claim_parser, False)
    get_signer_for_claim_parser.add_argument(
        "--claim-id", required=True, help="Type: uint256", type=int
    )
    get_signer_for_claim_parser.set_defaults(func=handle_get_signer_for_claim)

    num_claims_parser = subcommands.add_parser("num-claims")
    add_default_arguments(num_claims_parser, False)
    num_claims_parser.set_defaults(func=handle_num_claims)

    on_erc1155_batch_received_parser = subcommands.add_parser(
        "on-erc1155-batch-received"
    )
    add_default_arguments(on_erc1155_batch_received_parser, True)
    on_erc1155_batch_received_parser.add_argument(
        "--arg1", required=True, help="Type: address"
    )
    on_erc1155_batch_received_parser.add_argument(
        "--arg2", required=True, help="Type: address"
    )
    on_erc1155_batch_received_parser.add_argument(
        "--arg3", required=True, help="Type: uint256[]", nargs="+"
    )
    on_erc1155_batch_received_parser.add_argument(
        "--arg4", required=True, help="Type: uint256[]", nargs="+"
    )
    on_erc1155_batch_received_parser.add_argument(
        "--arg5", required=True, help="Type: bytes", type=bytes_argument_type
    )
    on_erc1155_batch_received_parser.set_defaults(func=handle_on_erc1155_batch_received)

    on_erc1155_received_parser = subcommands.add_parser("on-erc1155-received")
    add_default_arguments(on_erc1155_received_parser, True)
    on_erc1155_received_parser.add_argument(
        "--arg1", required=True, help="Type: address"
    )
    on_erc1155_received_parser.add_argument(
        "--arg2", required=True, help="Type: address"
    )
    on_erc1155_received_parser.add_argument(
        "--arg3", required=True, help="Type: uint256", type=int
    )
    on_erc1155_received_parser.add_argument(
        "--arg4", required=True, help="Type: uint256", type=int
    )
    on_erc1155_received_parser.add_argument(
        "--arg5", required=True, help="Type: bytes", type=bytes_argument_type
    )
    on_erc1155_received_parser.set_defaults(func=handle_on_erc1155_received)

    on_erc721_received_parser = subcommands.add_parser("on-erc721-received")
    add_default_arguments(on_erc721_received_parser, True)
    on_erc721_received_parser.add_argument(
        "--operator", required=True, help="Type: address"
    )
    on_erc721_received_parser.add_argument(
        "--from-arg", required=True, help="Type: address"
    )
    on_erc721_received_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    on_erc721_received_parser.add_argument(
        "--data", required=True, help="Type: bytes", type=bytes_argument_type
    )
    on_erc721_received_parser.set_defaults(func=handle_on_erc721_received)

    owner_parser = subcommands.add_parser("owner")
    add_default_arguments(owner_parser, False)
    owner_parser.set_defaults(func=handle_owner)

    paused_parser = subcommands.add_parser("paused")
    add_default_arguments(paused_parser, False)
    paused_parser.set_defaults(func=handle_paused)

    renounce_ownership_parser = subcommands.add_parser("renounce-ownership")
    add_default_arguments(renounce_ownership_parser, True)
    renounce_ownership_parser.set_defaults(func=handle_renounce_ownership)

    set_claim_status_parser = subcommands.add_parser("set-claim-status")
    add_default_arguments(set_claim_status_parser, True)
    set_claim_status_parser.add_argument(
        "--claim-id", required=True, help="Type: uint256", type=int
    )
    set_claim_status_parser.add_argument(
        "--status", required=True, help="Type: bool", type=boolean_argument_type
    )
    set_claim_status_parser.set_defaults(func=handle_set_claim_status)

    set_signer_for_claim_parser = subcommands.add_parser("set-signer-for-claim")
    add_default_arguments(set_signer_for_claim_parser, True)
    set_signer_for_claim_parser.add_argument(
        "--claim-id", required=True, help="Type: uint256", type=int
    )
    set_signer_for_claim_parser.add_argument(
        "--signer-arg", required=True, help="Type: address"
    )
    set_signer_for_claim_parser.set_defaults(func=handle_set_signer_for_claim)

    supports_interface_parser = subcommands.add_parser("supports-interface")
    add_default_arguments(supports_interface_parser, False)
    supports_interface_parser.add_argument(
        "--interface-id", required=True, help="Type: bytes4", type=bytes_argument_type
    )
    supports_interface_parser.set_defaults(func=handle_supports_interface)

    terminus_address_parser = subcommands.add_parser("terminus-address")
    add_default_arguments(terminus_address_parser, False)
    terminus_address_parser.set_defaults(func=handle_terminus_address)

    transfer_ownership_parser = subcommands.add_parser("transfer-ownership")
    add_default_arguments(transfer_ownership_parser, True)
    transfer_ownership_parser.add_argument(
        "--new-owner", required=True, help="Type: address"
    )
    transfer_ownership_parser.set_defaults(func=handle_transfer_ownership)

    withdraw_erc1155_parser = subcommands.add_parser("withdraw-erc1155")
    add_default_arguments(withdraw_erc1155_parser, True)
    withdraw_erc1155_parser.add_argument(
        "--token-address", required=True, help="Type: address"
    )
    withdraw_erc1155_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    withdraw_erc1155_parser.add_argument(
        "--amount", required=True, help="Type: uint256", type=int
    )
    withdraw_erc1155_parser.set_defaults(func=handle_withdraw_erc1155)

    withdraw_erc20_parser = subcommands.add_parser("withdraw-erc20")
    add_default_arguments(withdraw_erc20_parser, True)
    withdraw_erc20_parser.add_argument(
        "--token-address", required=True, help="Type: address"
    )
    withdraw_erc20_parser.add_argument(
        "--amount", required=True, help="Type: uint256", type=int
    )
    withdraw_erc20_parser.set_defaults(func=handle_withdraw_erc20)

    withdraw_erc721_parser = subcommands.add_parser("withdraw-erc721")
    add_default_arguments(withdraw_erc721_parser, True)
    withdraw_erc721_parser.add_argument(
        "--token-address", required=True, help="Type: address"
    )
    withdraw_erc721_parser.add_argument(
        "--token-id", required=True, help="Type: uint256", type=int
    )
    withdraw_erc721_parser.set_defaults(func=handle_withdraw_erc721)

    return parser


def main() -> None:
    parser = generate_cli()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
