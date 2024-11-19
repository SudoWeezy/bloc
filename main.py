from algokit_utils.beta.algorand_client import (
    AlgorandClient,
    AssetCreateParams,
    AssetOptInParams,
    AssetTransferParams,
    PayParams
)
from algosdk import error

# Client to connect to localnet
client = AlgorandClient.default_local_net()

# Import dispenser from KMD
dispenser_acct = client.account.dispenser()

print("Dispenser account", dispenser_acct.address)

# Create an account
creator_acct = client.account.random()
print("Creator address", creator_acct.address)

## Fund creator account
client.send.payment(
    PayParams(
        sender=dispenser_acct.address,
        receiver=creator_acct.address,
        amount=10_000_000
    )
)

# Create a token
asset_create_txn_sent = client.send.asset_create(
    AssetCreateParams(
        sender=creator_acct.address,
        total=1000,
        asset_name="bloc token",
        unit_name="btok",
        manager=creator_acct.address,
        clawback=creator_acct.address,
        freeze=creator_acct.address,
        reserve=creator_acct.address,
        default_frozen=False, # handle by composer
        decimals=0 # handle by composer
    )
)

# Get the Asset Id
asset_id = asset_create_txn_sent["confirmation"]["asset-index"]
print("Asset ID:", asset_id)


# Create receiver account
receiver_acct = client.account.random()



# Transfer Asset
try:
    asset_transfer_txn_sent = client.send.asset_transfer(
        AssetTransferParams(
            sender=creator_acct.address,
            receiver=receiver_acct.address,
            asset_id=asset_id,
            amount=10
        )
    )
except error.AlgodHTTPError as e:
    print(e)


## Create Atomic transaction
group_txn = client.new_group()
### Opt-in
group_txn.add_asset_opt_in(
    AssetOptInParams(
        sender=receiver_acct.address,
        asset_id=asset_id,
    )
)
### Pay the creator for token
group_txn.add_payment(
    PayParams(
        sender=receiver_acct.address,
        receiver=creator_acct.address,
        amount = 1_000_000
    )
)


### Transfer tokens
group_txn.add_asset_transfer(
    AssetTransferParams(
        sender=creator_acct.address,
        receiver=receiver_acct.address,
        asset_id=asset_id,
        amount=10
    )
)

### Send Atomic Transaction
group_txn.execute()


## Display
print("Creator Info" ,client.account.get_information(creator_acct.address))

print("Receiver Info" ,client.account.get_information(receiver_acct.address))
