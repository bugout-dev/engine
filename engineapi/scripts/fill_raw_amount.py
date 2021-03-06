import argparse

from brownie import network, Contract
from typing import Dict, List, Optional, Any

from .. import db
from ..settings import BLOCKCHAINS_TO_BROWNIE_NETWORKS
from ..Dropper import Dropper
from ..MockErc20 import MockErc20


def run_fill_raw_amount(args: argparse.Namespace):
    # sync raw_amount column with amount column

    # create chache of claim token type
    # newtwork contract and list of claims with their token type

    token_tytes: Dict[str, Dict[str, List[Dict[str, Any]]]] = dict()

    with db.yield_db_session_ctx() as db_session:

        res = db_session.execute(
            """select distinct dropper_contracts.blockchain, dropper_contracts.address, dropper_claims.claim_id from dropper_contracts 
                            left join dropper_claims on dropper_contracts.id = dropper_claims.dropper_contract_id
                            where dropper_claims.claim_id is not null"""
        )
        results = res.fetchall()

        for blockchain, address, claim_id in results:
            if blockchain not in token_tytes:
                token_tytes[blockchain] = dict()
            if address not in token_tytes[blockchain]:
                token_tytes[blockchain][address] = list()
            token_tytes[blockchain][address].append(claim_id)

        db_session.execute(
            """
            create table temptest
            (
                blockchain varchar, 
                address varchar, 
                claim_id varchar,
                token_type varchar,
                zeros varchar
            )
                
            """
        )

        for blockchain in token_tytes:
            brownie_network = BLOCKCHAINS_TO_BROWNIE_NETWORKS.get(blockchain)
            network.connect(brownie_network)
            for address in token_tytes[blockchain]:
                dropper_contract: Optional[Contract] = Dropper(address)

                for claim_id in token_tytes[blockchain][address]:
                    claim_info = dropper_contract.get_claim(claim_id)
                    zeros = None
                    if claim_info[0] == 20:
                        erc20_contract: Optional[Contract] = MockErc20(claim_info[1])
                        zeros = "0" * erc20_contract.decimals()

                    db_session.execute(
                        """
                                insert into temptest
                                (
                                    blockchain, 
                                    address, 
                                    claim_id,
                                    token_type,
                                    zeros

                                )
                                values
                                (
                                    :blockchain, 
                                    :address, 
                                    :claim_id,
                                    :token_type,
                                    :zeros
                                )
                                """,
                        {
                            "blockchain": blockchain,
                            "address": address,
                            "claim_id": str(claim_id),
                            "token_type": str(claim_info[0]),
                            "zeros": zeros,
                        },
                    )

            network.disconnect()

        db_session.commit()

        # update raw_amount column
        db_session.execute(
            """
            update
                dropper_claimants
            set
                raw_amount = (
                    CASE
                        WHEN (
                            select
                                DISTINCT temptest.token_type
                            from
                                temptest
                                inner join dropper_claims ON temptest.claim_id :: int = dropper_claims.claim_id
                            where
                                dropper_claims.id = dropper_claimants.dropper_claim_id
                        ) :: int = 20 THEN CASE
                            WHEN dropper_claimants.amount is not null
                            and dropper_claimants.amount > 0 THEN CONCAT(
                                CAST(dropper_claimants.amount as varchar),
                                    (
                                        select
                                            temptest.zeros
                                        from
                                            temptest
                                            inner join dropper_claims ON temptest.claim_id :: int = dropper_claims.claim_id
                                        where
                                            dropper_claims.id = dropper_claimants.dropper_claim_id
                                    )
                                )
                                WHEN true THEN CAST(dropper_claimants.amount as varchar)
                            END
                            WHEN true THEN CAST(dropper_claimants.amount as varchar)
                        END
                    );
            """
        )
        db_session.commit()


def main():
    parser = argparse.ArgumentParser(
        description="dao: The command line interface to Moonstream DAO"
    )
    parser.set_defaults(func=lambda _: parser.print_help())
    subparsers = parser.add_subparsers()

    run_fill_raw_amount_parser = subparsers.add_parser(
        "fill_raw_amount", help="Fill raw_amount column"
    )

    run_fill_raw_amount_parser.set_defaults(func=run_fill_raw_amount)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
