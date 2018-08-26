import re

from django.shortcuts import render, redirect,reverse
from django.core.files import File
import time
import json
from eth_account import account
from hexbytes import HexBytes
from web3 import Web3
from .ethereum_network import  web3
from .ethereum_network import send_transaction


# Create your views here.
def home(request):
    return render(request,'home.html')


def new_wallet(request):
    if request.method == "GET":
        return render(request,'home.html')
    else:
        data = {}
        password = request.POST.get("password")
        acc = account.Account.create()
        address = acc.address
        data["address"] = address
        private_key = acc.privateKey
        account_data = account.Account.encrypt(private_key, password)
        keystore = json.dumps(account_data)
        data["keystore"] = keystore
        time_now = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        filename = "UTC--" + time_now + "_" + address
        data["filename"] = filename
        return render(request,'new_wallet.html',context=data)


def balance(request):
    if request.method == "GET":
        return render(request,'balance.html')
    else:
        data = {}
        keystore_file = request.FILES.get("keystore")
        keystore = keystore_file.read().decode('utf-8')
        print(keystore,type(keystore))
        dict_keystore = eval(keystore)
        from_address = Web3.toChecksumAddress('0x'+dict_keystore["address"])
        data["address"] = from_address
        request.session["dict_keystore"] = dict_keystore
        request.session["from_address"] = from_address
        data["balance"] = Web3.fromWei(web3.eth.getBalance(from_address),"ether")
        return render(request,'transaction.html',context=data)


def transaction(request):
    if request.method=="GET":
        return render(request,'transaction.html')
    else:
        dict_keystore = request.session["dict_keystore"]
        from_address = request.session['from_address']
        to_address = request.POST.get("to_address")
        if dict_keystore and from_address and to_address:
            print(">>>>>>>", dict_keystore)
            to_address = Web3.toChecksumAddress(to_address)
            # assert Web3.isAddress(to_address),"invalid address"
            value = Web3.toWei(float(request.POST.get("value")),'ether')
            print("value",value)
            gas_limit = int(request.POST.get("gas"))
            print("gaslimit",gas_limit)
            gas_price = int(request.POST.get("gas_price"))
            print("gaslimit", gas_price)
            password = request.POST.get("password")
            print(">>>>>>>>>pw",password)
            privatekey = HexBytes(
                account.Account.decrypt(dict_keystore, password))  ##convert the binary private key to hex type
            pk = privatekey.hex()
            print(">>>>>>>>>pk",pk)
            txhash_b =send_transaction(from_address,to_address,value,gas_price,gas_limit,pk)
            txhash = HexBytes(txhash_b).hex()
            data = {}
            data["txn"] = txhash
            print(txhash)
            return render(request,'outcome.html',context=data)

        else:
            return redirect(reverse("balance"))




