import requests
from time import sleep
from flask import Flask, request, jsonify

app = Flask(__name__)


def pay(iban, amount, type_):
    data = {
        'wallet_id': iban,
        'type': type_,
        'iban': 'iban',
        'amount': str(amount)
    }
    url = f'http://127.0.0.1:5000/settle'
    response = requests.post(url, json=data)
    response_json = response.json()
    if not response_json['result'] == 'success':
        raise Exception(f'Error cannot {type} money, iban = {iban}')


def create_wallet(id):
    url = f'http://127.0.0.1:5000/wallet/{id}'
    response = (requests.post(url)).json()
    if not response['result'] == 'success':
        print(f'Wallet {id} already exist')
    else:
        print(f'Wallet {id} created')


def setup_wallets(iban_lst):
    amount = 100000 # will be pretty rich :)
    for iban in iban_lst:
        create_wallet(iban)
        pay(iban, amount, 'payin')  # add some cash in wallets





@app.route('/transfer', methods=['POST', 'GET'])
def transfer():
    if request.method == 'POST':
        data = request.json
        from_iban = data['from_iban']
        to_iban = data['to_iban']
        amount = data['amount']
        # setup_wallets([from_iban, to_iban])
        pay(to_iban, amount, 'payout')
        pay(from_iban, amount, 'payin')
        return jsonify(dict(result='success', message='Transfer completed!'))

    return jsonify(dict(result='success', message='Nothing is here'))