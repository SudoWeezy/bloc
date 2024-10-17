"""
Test Summary for Digital Marketplace Smart Contract:

1. **Account Funding**:
   - The dispenser funds both the creator and buyer accounts with ALGO for testing purposes.

2. **Asset Creation**:
   - The creator account creates a new asset with a total supply of 10 units.

3. **App Opt-In to Asset**:
   - The smart contract application opts in to hold the created asset after receiving ALGO to cover Minimum Balance Requirement (MBR).

4. **Asset Transfer to App**:
   - The creator transfers 3 units of the asset to the smart contract application.

5. **Set Asset Price**:
   - The smart contract sets a unitary price of 3.3 ALGO for the asset.

6. **Buyer Opt-In and Purchase**:
   - The buyer opts into the asset and purchases 2 units from the smart contract by transferring 6.6 ALGO.

7. **Application Deletion**:
   - The smart contract is deleted, and any unsold assets and remaining ALGO are returned to the creator account.
"""

import algokit_utils
import algosdk
import pytest
from algokit_utils.beta.account_manager import AddressAndSigner
from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams,
)
from algosdk.atomic_transaction_composer import TransactionWithSigner

from smart_contracts.artifacts.digital_marketplace.digital_marketplace_client import (
    DigitalMarketplaceClient,
)


# Fixture to create an Algorand client that connects to the local test network
@pytest.fixture(scope="session")
def algorand() -> AlgorandClient:
    """Get an AlgorandClient to use throughout the tests"""
    return AlgorandClient.default_local_net()


# Fixture to get the dispenser account to fund test accounts
@pytest.fixture(scope="session")
def dispenser(algorand: AlgorandClient) -> AddressAndSigner:
    """Get the dispenser to fund test addresses"""
    return algorand.account.dispenser()


# Fixture to create a random account for the creator and fund it with ALGO
@pytest.fixture(scope="session")
def creator(algorand: AlgorandClient, dispenser: AddressAndSigner) -> AddressAndSigner:
    acct = algorand.account.random()
    # Fund the newly created account with 10 ALGO from the dispenser
    algorand.send.payment(
        PayParams(sender=dispenser.address, receiver=acct.address, amount=10_000_000)
    )

    return acct


# Fixture to create a test asset using the creator account
@pytest.fixture(scope="session")
def test_asset_id(creator: AddressAndSigner, algorand: AlgorandClient) -> int:
    # Create an asset with a total supply of 10 units
    sent_txn = algorand.send.asset_create(
        AssetCreateParams(sender=creator.address, total=10)
    )

    # Return the asset ID after the transaction is confirmed
    return sent_txn["confirmation"]["asset-index"]


# Fixture to instantiate the Digital Marketplace smart contract client
@pytest.fixture(scope="session")
def digital_marketplace_client(
    algorand: AlgorandClient, creator: AddressAndSigner, test_asset_id: int
) -> DigitalMarketplaceClient:
    """Instantiate an application client we can use for our tests"""
    client = DigitalMarketplaceClient(
        algod_client=algorand.client.algod,
        sender=creator.address,
        signer=creator.signer,
    )

    # Deploy the marketplace smart contract on the network
    client.create_create_application(unitary_price=0, asset_id=test_asset_id)

    return client


# Test case to ensure the application can opt-in to an asset
def test_opt_in_to_asset(
    digital_marketplace_client: DigitalMarketplaceClient,
    creator: AddressAndSigner,
    test_asset_id: int,
    algorand: AlgorandClient,
):
    # Ensure the app has not yet opted in to the asset (raises an error if it hasn't)
    pytest.raises(
        algosdk.error.AlgodHTTPError,
        lambda: algorand.account.get_asset_information(
            digital_marketplace_client.app_address, test_asset_id
        ),
    )

    # Send 200_000 uALGO to the app to cover the Minimum Balance Requirement (MBR)
    mbr_pay_txn = algorand.transactions.payment(
        PayParams(
            sender=creator.address,
            receiver=digital_marketplace_client.app_address,
            amount=200_000,
            extra_fee=1_000,
        )
    )

    # The app opts into the asset
    result = digital_marketplace_client.opt_in_to_asset(
        mbr_pay=TransactionWithSigner(txn=mbr_pay_txn, signer=creator.signer),
        transaction_parameters=algokit_utils.TransactionParameters(
            # The asset ID must be declared for the Algorand Virtual Machine (AVM) to use it
            foreign_assets=[test_asset_id]
        ),
    )

    # Ensure the transaction is confirmed in a round
    assert result.confirmed_round

    # Verify that the app has opted in to the asset (but doesn't hold any yet)
    assert (
        algorand.account.get_asset_information(
            digital_marketplace_client.app_address, test_asset_id
        )["asset-holding"]["amount"]
        == 0
    )


# Test case to transfer assets to the smart contract app
def test_deposit(
    digital_marketplace_client: DigitalMarketplaceClient,
    creator: AddressAndSigner,
    test_asset_id: int,
    algorand: AlgorandClient,
):
    # Transfer 3 units of the asset from the creator to the app
    result = algorand.send.asset_transfer(
        AssetTransferParams(
            sender=creator.address,
            receiver=digital_marketplace_client.app_address,
            asset_id=test_asset_id,
            amount=3,
        )
    )

    # Ensure the asset transfer transaction was successful
    assert result["confirmation"]

    # Verify that the app now holds 3 units of the asset
    assert (
        algorand.account.get_asset_information(
            digital_marketplace_client.app_address, test_asset_id
        )["asset-holding"]["amount"]
        == 3
    )


# Test case to set the price of assets within the smart contract
def test_set_price(digital_marketplace_client: DigitalMarketplaceClient):
    # Set the unitary price of the asset to 3.3 ALGO (3_300_000 microALGO)
    result = digital_marketplace_client.set_price(unitary_price=3_300_000)

    # Ensure the price-setting transaction was confirmed
    assert result.confirmed_round


# Test case to simulate a buyer purchasing assets from the app
def test_buy(
    digital_marketplace_client: DigitalMarketplaceClient,
    creator: AddressAndSigner,
    test_asset_id: int,
    algorand: AlgorandClient,
    dispenser: AddressAndSigner,
):
    # Create a new random account to act as the buyer
    buyer = algorand.account.random()

    # Fund the buyer account with 10 ALGO using the dispenser
    algorand.send.payment(
        PayParams(sender=dispenser.address, receiver=buyer.address, amount=10_000_000)
    )

    # Opt the buyer into the asset
    algorand.send.asset_opt_in(
        AssetOptInParams(sender=buyer.address, asset_id=test_asset_id)
    )

    # Form a payment transaction for the buyer to purchase 2 units of the asset (2 * 3.3 ALGO)
    buyer_payment_txn = algorand.transactions.payment(
        PayParams(
            sender=buyer.address,
            receiver=digital_marketplace_client.app_address,
            amount=2 * 3_300_000,
            extra_fee=1_000,
        )
    )

    # Execute the buy operation on the app
    result = digital_marketplace_client.buy(
        buyer_txn=TransactionWithSigner(txn=buyer_payment_txn, signer=buyer.signer),
        quantity=2,
        transaction_parameters=algokit_utils.TransactionParameters(
            sender=buyer.address,
            signer=buyer.signer,
            # Inform the AVM that the transaction uses this asset
            foreign_assets=[test_asset_id],
        ),
    )

    # Ensure the transaction was confirmed in a round
    assert result.confirmed_round

    # Verify that the buyer now holds 2 units of the asset
    assert (
        algorand.account.get_asset_information(buyer.address, test_asset_id)[
            "asset-holding"
        ]["amount"]
        == 2
    )


# Test case to delete the application and retrieve the remaining assets and funds
def test_delete_application(
    digital_marketplace_client: DigitalMarketplaceClient,
    creator: AddressAndSigner,
    test_asset_id: int,
    algorand: AlgorandClient,
):
    # sk = creator.signer.private_key
    # print(algosdk.mnemonic.from_private_key(sk))
    # print("Set fees at 0,003")
    # assert False

    # Get the balance of the creator before the app is deleted
    before_call_amount = algorand.account.get_information(creator.address)["amount"]

    # Set custom transaction parameters for deletion
    sp = algorand.client.algod.suggested_params()
    sp.flat_fee = True
    sp.fee = 3_000

    # Delete the smart contract application
    result = digital_marketplace_client.delete_delete_application(
        transaction_parameters=algokit_utils.TransactionParameters(
            # Tell the AVM that the transaction involves this asset
            foreign_assets=[test_asset_id],
            suggested_params=sp,
        )
    )

    # Ensure the deletion transaction was confirmed in a round
    assert result.confirmed_round

    # Get the balance of the creator after the app is deleted
    after_call_amount = algorand.account.get_information(creator.address)["amount"]

    # Verify that the creator received the remaining funds and unsold assets
    # Creator should receive: (2 * 3_300_000 ALGO from sales) + (200_000 MBR refund) - (3_000 fee)
    assert after_call_amount - before_call_amount == (2 * 3_300_000) + 200_000 - 3_000

    # The creator should receive 8 unsold assets back (since 2 were sold)
    assert (
        algorand.account.get_asset_information(creator.address, test_asset_id)[
            "asset-holding"
        ]["amount"]
        == 8
    )
