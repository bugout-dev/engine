import unittest
from venv import create

from brownie import accounts, network
from brownie.exceptions import VirtualMachineError
from . import Lootbox, MockTerminus, MockErc20
from .core import lootbox_item_to_tuple, gogogo


class LootboxTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        try:
            network.connect()
        except:
            pass

        cls.terminus = MockTerminus.MockTerminus(None)
        cls.terminus.deploy({"from": accounts[0]})

        cls.erc20_contracts = [MockErc20.MockErc20(None) for _ in range(5)]
        for contract in cls.erc20_contracts:
            contract.deploy({"from": accounts[0]})

        cls.erc20_contracts[0].mint(accounts[0], 100 * 10 ** 18, {"from": accounts[0]})

        cls.terminus.set_payment_token(
            cls.erc20_contracts[0].address, {"from": accounts[0]}
        )
        cls.terminus.set_pool_base_price(1, {"from": accounts[0]})

        gogogo_result = gogogo(cls.terminus.address, {"from": accounts[0]})
        cls.lootbox = Lootbox.Lootbox(gogogo_result["Lootbox"])
        cls.admin_token_pool_id = gogogo_result["adminTokenPoolId"]

        for i in range(5):
            cls.erc20_contracts[i].mint(
                cls.lootbox.address,
                (100 ** 18) * (10 ** 18),
                {"from": accounts[0]},
            )

    def _create_terminus_pool(
        self, capacity=10 ** 18, transferable=True, burnable=True
    ) -> int:
        self.terminus.create_pool_v1(
            capacity,
            transferable,
            burnable,
            {"from": accounts[0]},
        )

        return self.terminus.total_pools()

    def _open_lootbox(self, account, lootboxId, count=None):
        """
        Open lootboxes with the given lootboxId and count.
        If count is None, open all available lootboxes.
        """
        lootbox_items_count = self.lootbox.lootbox_item_count(lootboxId)
        lootbox_terminus_pool_id = self.lootbox.terminus_pool_idby_lootbox_id(lootboxId)

        if count is None:
            count = self.terminus.balance_of(account.address, lootbox_terminus_pool_id)

        for i in range(lootbox_items_count):
            (
                reward_type,
                token_address,
                token_id,
                token_amount,
            ) = self.lootbox.get_lootbox_item_by_index(lootboxId, i)

            claimer_lootbox_balance_before = self.terminus.balance_of(
                account.address, lootbox_terminus_pool_id
            )

            if reward_type == 20:
                mockErc20 = MockErc20.MockErc20(token_address)

                contract_balance_before = mockErc20.balance_of(self.lootbox.address)
                claimer_balance_before = mockErc20.balance_of(account.address)

                # TODO remove this shit
                network.chain.snapshot()
                self.lootbox.open_lootbox(lootboxId, count, {"from": account})

                contract_balance_after = mockErc20.balance_of(self.lootbox.address)
                claimer_balance_after = mockErc20.balance_of(account.address)

                self.assertEqual(
                    contract_balance_before - contract_balance_after,
                    token_amount * count,
                )
                self.assertEqual(
                    claimer_balance_after - claimer_balance_before,
                    token_amount * count,
                )

            elif reward_type == 1155:
                raise NotImplementedError
                mockErc1155 = MockTerminus.MockTerminus(token_address)
                contract_balance_before = mockErc1155.balance_of(self.lootbox.address)
                claimer_balance_before = mockErc1155.balance_of(account.address)

                self.lootbox.open_lootbox(lootboxId, count, {"from": account})

                contract_balance_after = mockErc1155.balance_of(self.lootbox.address)
                claimer_balance_after = mockErc1155.balance_of(account.address)

                self.assertEqual(
                    contract_balance_before - contract_balance_after,
                    token_amount * count,
                )
                self.assertEqual(
                    claimer_balance_after - claimer_balance_before,
                    token_amount * count,
                )

            else:
                raise ValueError(f"Unknown reward type: {reward_type}")

            self.assertEqual(
                claimer_lootbox_balance_before
                - self.terminus.balance_of(account.address, lootbox_terminus_pool_id),
                count,
            )
            network.chain.revert()


class LootboxBaseTest(LootboxTestCase):
    def test_lootbox_create_with_single_item(self):

        lootboxes_count_0 = self.lootbox.total_lootbox_count()

        self.lootbox.create_lootbox(
            [
                lootbox_item_to_tuple(
                    reward_type=20,
                    token_address=self.erc20_contracts[1].address,
                    token_id=0,
                    token_amount=10 * 10 ** 18,
                )
            ],
            {"from": accounts[0]},
        )

        self.erc20_contracts[1].mint(
            self.lootbox.address, 100 * 10 ** 18, {"from": accounts[0]}
        )

        lootboxes_count_1 = self.lootbox.total_lootbox_count()
        created_lootbox_id = self.lootbox.total_lootbox_count() - 1

        self.assertEqual(lootboxes_count_1, lootboxes_count_0 + 1)

        self.assertEqual(self.lootbox.lootbox_item_count(created_lootbox_id), 1)

        self.assertEqual(
            self.lootbox.get_lootbox_item_by_index(created_lootbox_id, 0),
            (20, self.erc20_contracts[1].address, 0, 10 * 10 ** 18),
        )

        self.lootbox.batch_mint_lootboxes(
            created_lootbox_id, [accounts[1].address], [1], {"from": accounts[0]}
        )

        self._open_lootbox(accounts[1], created_lootbox_id, 1)

    def test_test_batch_mint_lootboxes(self):

        self.lootbox.create_lootbox(
            [
                lootbox_item_to_tuple(
                    reward_type=20,
                    token_address=self.erc20_contracts[1].address,
                    token_id=0,
                    token_amount=10 * 10 ** 18,
                )
            ],
            {"from": accounts[0]},
        )

        lootbox_id = self.lootbox.total_lootbox_count() - 1

        self.lootbox.batch_mint_lootboxes(
            lootbox_id,
            [accounts[1].address, accounts[2].address, accounts[3].address],
            [1, 2, 3],
            {"from": accounts[0]},
        )

        balances = [
            self.lootbox.get_lootbox_balance(lootbox_id, accounts[1].address),
            self.lootbox.get_lootbox_balance(lootbox_id, accounts[2].address),
            self.lootbox.get_lootbox_balance(lootbox_id, accounts[3].address),
        ]

        self.assertEqual(balances, [1, 2, 3])

    def test_lootbox_create_with_multiple_items(self):

        erc20_rewards = [
            lootbox_item_to_tuple(
                reward_type=20,
                token_address=self.erc20_contracts[i].address,
                token_id=0,
                token_amount=i * 15 * 10 ** 18,
            )
            for i in range(3)
        ]

        lootbox_items = erc20_rewards

        self.lootbox.create_lootbox(lootbox_items, {"from": accounts[0]})
        lootbox_id = self.lootbox.total_lootbox_count() - 1

        self.lootbox.batch_mint_lootboxes(
            lootbox_id,
            [accounts[1].address, accounts[2].address, accounts[3].address],
            [1, 2, 3],
            {"from": accounts[0]},
        )
        self.assertEqual(self.lootbox.get_lootbox_balance(lootbox_id, accounts[1]), 1)

        terminus_pool_id = self.lootbox.terminus_pool_idby_lootbox_id(lootbox_id)
        self.assertEqual(
            self.terminus.balance_of(accounts[1].address, terminus_pool_id), 1
        )

        # self.lootbox.open_lootbox(lootbox_id, 1, {"from": accounts[1]})
        self._open_lootbox(accounts[1], lootbox_id, 1)

        self._open_lootbox(accounts[2], lootbox_id, 1)
        self._open_lootbox(accounts[2], lootbox_id, 1)

        self._open_lootbox(accounts[3], lootbox_id, 3)
        # with self.assertRaises(Exception):
        #    self._open_lootbox(accounts[3], lootbox_id, 1)


class LootboxACLTests(LootboxTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.lootbox.grant_admin_role(accounts[1].address, {"from": accounts[0]})

    def test_nonadmin_cannot_create_lootbox(self):
        lootboxes_count_0 = self.lootbox.total_lootbox_count()
        with self.assertRaises(VirtualMachineError):
            self.lootbox.create_lootbox(
                [
                    lootbox_item_to_tuple(
                        reward_type=20,
                        token_address=self.erc20_contracts[1].address,
                        token_id=0,
                        token_amount=10 * 10 ** 18,
                    )
                ],
                {"from": accounts[2]},
            )
        lootboxes_count_1 = self.lootbox.total_lootbox_count()
        self.assertEqual(lootboxes_count_1, lootboxes_count_0)

    def test_admin_can_create_and_mint_working_lootbox(self):
        lootboxes_count_0 = self.lootbox.total_lootbox_count()

        self.lootbox.create_lootbox(
            [
                lootbox_item_to_tuple(
                    reward_type=20,
                    token_address=self.erc20_contracts[1].address,
                    token_id=0,
                    token_amount=10 * 10 ** 18,
                )
            ],
            {"from": accounts[1]},
        )

        self.erc20_contracts[1].mint(
            self.lootbox.address, 100 * 10 ** 18, {"from": accounts[0]}
        )

        lootboxes_count_1 = self.lootbox.total_lootbox_count()
        created_lootbox_id = self.lootbox.total_lootbox_count() - 1

        self.assertEqual(lootboxes_count_1, lootboxes_count_0 + 1)

        self.assertEqual(self.lootbox.lootbox_item_count(created_lootbox_id), 1)

        self.assertEqual(
            self.lootbox.get_lootbox_item_by_index(created_lootbox_id, 0),
            (20, self.erc20_contracts[1].address, 0, 10 * 10 ** 18),
        )

        self.lootbox.batch_mint_lootboxes(
            created_lootbox_id, [accounts[3].address], [1], {"from": accounts[1]}
        )

        recipient_erc20_balance_0 = self.erc20_contracts[1].balance_of(accounts[3].address)
        self.lootbox.open_lootbox(created_lootbox_id, 1, {"from": accounts[3]})
        recipient_erc20_balance_1 = self.erc20_contracts[1].balance_of(accounts[3].address)
        self.assertEqual(recipient_erc20_balance_1, recipient_erc20_balance_0 + (10 * (10**18)))

    def test_nonadmin_cannot_mint_lootbox_created_by_admin(self):
        lootboxes_count_0 = self.lootbox.total_lootbox_count()

        self.lootbox.create_lootbox(
            [
                lootbox_item_to_tuple(
                    reward_type=20,
                    token_address=self.erc20_contracts[1].address,
                    token_id=0,
                    token_amount=10 * 10 ** 18,
                )
            ],
            {"from": accounts[1]},
        )

        self.erc20_contracts[1].mint(
            self.lootbox.address, 100 * 10 ** 18, {"from": accounts[0]}
        )

        lootboxes_count_1 = self.lootbox.total_lootbox_count()
        created_lootbox_id = self.lootbox.total_lootbox_count() - 1

        self.assertEqual(lootboxes_count_1, lootboxes_count_0 + 1)
        self.assertEqual(self.lootbox.lootbox_item_count(created_lootbox_id), 1)

        with self.assertRaises(VirtualMachineError):
            self.lootbox.batch_mint_lootboxes(
                created_lootbox_id, [accounts[3].address], [1], {"from": accounts[2]}
            )

if __name__ == "__main__":
    unittest.main()
