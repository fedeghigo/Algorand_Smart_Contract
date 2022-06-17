import json
import time
import base64
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction
import streamlit as st


st.title("Algorand Crowfunding")

import json
import time
import base64
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import transaction

from PIL import Image

image = Image.open("images/algoran.jpg")

st.image(image, caption="Algorand Logo")

st.info(
    "Dislaimer: This app is developed for Testing Purposes , we hadn't take care of Cybersecurity, please use dummy Waller"
)
st.info(
    "For use it we suggest to create a Wallet throught Algosigner https://www.purestake.com/  if you use chrome https://chrome.google.com/webstore/detail/algosigner/kmmolakhbgdlpkjkcjkebenjheonagdm"
)
st.info(
    "Create the Wallet in the Test Net, and fund it throught https://dispenser.testnet.aws.algodev.network/ "
)
st.info("After that you can play around; Enjoy!")
st.balloons()

algod_token = ALGOD_TOKEN
algod_address = ALGOD_ADDRESS  #'https://testnet-algorand.api.purestake.io/ps2'
purestake_token = {"X-Api-key": algod_token}


algodclient = algod.AlgodClient(algod_token, algod_address, headers=purestake_token)
params = algodclient.suggested_params()


st.write(params)


####
mnemonic_phrase = st.text_input("Insert the Mnemonic of your test account")
if st.button("Send"):
    # "blind asset click wide gaze wild cruel mountain volume truth jeans trash alien beauty charge ladder thank hammer shock laptop donkey hazard bronze abstract robot"
    account_private_key = mnemonic.to_private_key(mnemonic_phrase)
    account_public_key = mnemonic.to_public_key(mnemonic_phrase)
    st.success("Connected")
else:
    st.write("not sent")


gh = params.gh
first_valid_round = params.first
last_valid_round = params.last
fee = params.min_fee
send_amount = st.number_input("Money to send", value=10)
send_amount = send_amount * 10000
dd_ammount = send_amount / 1000000
st.write(f"The currently sending ammount is { dd_ammount} Algo")

try:
    existing_account = account_public_key
except:
    st.warning("Define Mnemonic Phrase")


####
send_to_address = SEND_TO_ADDRESS
st.write("The receiving crowfounding Wallet", send_to_address)
# Crowfounded account

###
try:
    tx = transaction.PaymentTxn(
        existing_account,
        fee,
        first_valid_round,
        last_valid_round,
        gh,
        send_to_address,
        send_amount,
        flat_fee=True,
    )
    signed_tx = tx.sign(account_private_key)
except:
    st.warning("Press send to start the transaction")


# Function from Algorand Inc. - utility for waiting on a transaction confirmation
def wait_for_confirmation(client, txid):
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round") > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction confirmed in round", txinfo.get("confirmed-round"))
    return txinfo


try:
    tx_confirm = algodclient.send_transaction(signed_tx)
    st.write("Transaction sent with ID", signed_tx.transaction.get_txid())
    wait_for_confirmation(algodclient, txid=signed_tx.transaction.get_txid())
    st.info(
        f"You could check the transaction at https://testnet.algoexplorer.io/tx/{tx_confirm}"
    )
except:
    st.info("More info on: https://pyteal.readthedocs.io/en/stable/")


st.info("Developed by Federico.I https://www.linkedin.com/in/federico-i-5336b0139/")
st.info("Thanks and Credit to Algorand https://www.algorand.com/")
st.info("Thanks and Credit to Purestake.io https://developer.purestake.io/home")
