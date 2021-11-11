import random
import json
import time
from web3 import Web3
# from statistics import mean


dict_ = {}
selected_people = []
value_selected = []
final_dict = {}




MAIN_URL = "https://mainnet.infura.io/v3/bb055071bba745488eda95512a6d0035"
# URL = 'https://8cf41633363c49a584fbfb0b556a5927.ropsten.rpc.rivet.cloud/'
URL = 'wss://ropsten.infura.io/ws/v3/bb055071bba745488eda95512a6d0035'

w3 = Web3(Web3.WebsocketProvider(URL))

wallet_address ="0xdB7633ad2E7cB296d5F4B2A5f6E90098327D2e04"
private_key = "d721601b61cc5dd2cb0c9e731d0822e1c8232e3a2859ff599522b564146bc812"
_public_key = Web3.toChecksumAddress("0xdB7633ad2E7cB296d5F4B2A5f6E90098327D2e04")
_nounce = w3.eth.get_transaction_count(_public_key)


# w3 = Web3(Web3.HTTPProvider(URL))


def _checking(_addr):
    '''
    ورودی تابع ک استرینگ است که چک میشمود ایا ادرس معبتری هست یا خیر
    false یا addrress درنهایت
    خارح میشود
    '''
    if not isinstance(_addr, str):
        print("ادرس بد وارد کردی باید یک استرینگ باشه")
        return False
    try:
        if not w3.isConnected():
            print("نت مشکل داره ")
            return False
        addr_ = Web3.toChecksumAddress(_addr)
        if not _addr:
            print("ادرس بدی وارد کردی شرمنده تم")
            return False
        return addr_
    except Exception as e:
        print(e)
        print("یه مشکلی وجود داره ×ـ× مثلا نتت ضعیفه")
        return False


def balance(_addr: str) -> float:
    """
    اینجا ادرس خواسته رو به تابع بدید
    توی خروجی یه عدد میده که همون باقیمانده ی حسابش هستش :)
    """
    addr_ = _checking(_addr)
    return float(w3.eth.get_balance(addr_) / 10 ** 18)


def transfer(_to_addr: str, _value: float, private_key: str, public_key: str, _nounce: int):
    to_addr_ = _checking(_to_addr)
    public_key = _checking(public_key)

    if to_addr_ and public_key:
        try:
            if balance(public_key) < _value:
                print("پول ت کمه ، نمیتونی کمک کنی ")
                return False
            p = w3.eth.gas_price

            trancation = {
                'from': public_key,
                'to': to_addr_,
                "gas": "0x200000",
                "gasPrice": p,
                "nonce": _nounce,
                "value": int(_value * 10 ** 18),
            }
            raw_trx = w3.eth.account.privateKeyToAccount(
                private_key).sign_transaction(trancation)
            res = w3.eth.send_raw_transaction(raw_trx.rawTransaction).hex()
            return res
        except Exception as e:
            print(e)
            print("یک اتفاقی افتاده که من نمیدونم ....")
            return 0


# Testing Functions with my wallet
# _public_key = Web3.toChecksumAddress("0xdB7633ad2E7cB296d5F4B2A5f6E90098327D2e04")
#
# print(balance("0xdB7633ad2E7cB296d5F4B2A5f6E90098327D2e04"))
#
#
# _nounce = w3.eth.get_transaction_count(_public_key)
# print(
#     transfer("0x926E29051d26C1b4Adec6912CCdbe24f8Dd578eF",
#              0.01,
#              "d721601b61cc5dd2cb0c9e731d0822e1c8232e3a2859ff599522b564146bc812",
#              "0xdB7633ad2E7cB296d5F4B2A5f6E90098327D2e04",
#              _nounce)
# )
# _nounce += 1
#
# time.sleep(5)
# print(balance("0x926E29051d26C1b4Adec6912CCdbe24f8Dd578eF"))


with open("wallets.json", "r") as w1:
    list_ = json.load(w1)
# print(list_[0], type(list_))
for i in range(10):
    selection_ = random.sample(list_, 10)
    value_selected.append(balance(selection_[i]))
    # value_selected.update(selection_:balance(selection_[i]))
    # value_selection = balance(selection_[i])
    # value_selected.append(value_selection)
    # dict_ = {k: v for k in selection_, for v in balance(selection_[i])}
    # dict_ = {tuple(selection_[i]): balance(selection_[i])}
    # print(dict_)
dict_people = dict(zip(selection_, value_selected))
print(dict_people)
mean_ = sum(value_selected)/len(value_selected)
# print(mean_)
cd = []
for q, w in dict_people.items():

    if w < mean_/10:
        a = transfer(q, 0.05, "d721601b61cc5dd2cb0c9e731d0822e1c8232e3a2859ff599522b564146bc812",
                     "0xdB7633ad2E7cB296d5F4B2A5f6E90098327D2e04", _nounce)
        _nounce += 1

"""
  بعد از ۵ ثانیه مجدد سمپل ها و موجودی همه(موارد کمتر از ۱۰ در صد میانگین و بقیه)رو در دبکشنری به فرمت جیسون ذخیره 
  میکنه 
"""
time.sleep(5)
for q, w in dict_people.items():
    final_dict[q] = balance(q)
print(final_dict)
# dict_people = dict(zip(selection_, value_selected))

with open("sent_money.json", "w") as sm:
    sm.write(json.dumps(final_dict))
