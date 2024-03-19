from flask import Flask, jsonify, request
import requests
import re
from datetime import datetime, timedelta
from googletrans import Translator

app = Flask(__name__)

def translate_variable(text, target_language='uk'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

def SendDateTOnewPost(ref):
    
    json_data = {
        "apiKey": "4ec45d6aaab94b72716c66b1df130dae",
        "modelName": "ScanSheet",
        "calledMethod": "insertDocuments",
        "methodProperties": {
            "Ref": "7a0fc714-dbec-11ee-a60f-48df37b921db",
            "Date": "01.04.2024",
            "DocumentRefs": [
                ref,
                "00000000-0000-0000-0000-000000000000"
            ]
        }
    }

    api_url = 'https://api.novaposhta.ua/v2.0/json/'

    response = requests.post(api_url, json=json_data)

    data = response.json()

    return data

def CretionNewDate(data):
    data_new = data
    
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    dataOfSend = tomorrow.strftime('%d.%m.%Y')

    phone_number = data_new['data']['Number'].lstrip('+')
    
    json_data = {
        "apiKey": "4ec45d6aaab94b72716c66b1df130dae",
        "modelName": "InternetDocument",
        "calledMethod": "save",
        "methodProperties": {
            "PayerType" : "Sender",
            "PaymentMethod" : "NonCash",
            "DateTime" : dataOfSend,
            "CargoType" : "Cargo",
            "VolumeGeneral" : "0.1",
            "Weight" : "0.2",
            "ServiceType" : "DoorsWarehouse",
            "SeatsAmount" : "2",
            "Description" : "Додатковий опис відправлення",
            "Cost" : "150",
            "CitySender" : "db5c88d0-391c-11dd-90d9-001a92567626",
            "Sender" : "df943600-9e53-11ee-a60f-48df37b921db",
            "SenderAddress" : "c3e95fb1-9fcd-11ee-a60f-48df37b921db",
            "ContactSender" : "73c4add6-9e58-11ee-a60f-48df37b921db",
            "SendersPhone" : "380631195959",
            "RecipientsPhone" : phone_number,
            "NewAddress" : data_new['data']['Nova_poshta_office_number'],
            "RecipientCityName" : translate_variable(data_new['data']['City']),
            "RecipientArea" : "",
            "RecipientAreaRegions" : "",
            "RecipientAddressName" : data_new['data']['Nova_poshta_office_number'],
            "RecipientHouse" : "",
            "RecipientFlat" : "",
            "RecipientName" : translate_variable(data_new['data']['Name']+" "+data_new['data']['MidelName']+" "+data_new['data']['FamilyName']),
            "RecipientType" : "PrivatePerson",
            "SettlementType" : "м.",
            "OwnershipForm" : "00000000-0000-0000-0000-000000000000",
            "RecipientContactName" : translate_variable(data_new['data']['Name']+" "+data_new['data']['MidelName']+" "+data_new['data']['FamilyName']),
            "EDRPOU" : "12345678"
        }
    }

    api_url = 'https://api.novaposhta.ua/v2.0/json/'

    response = requests.post(api_url, json=json_data)

    data = response.json()

    ref = data['data'][0]['Ref']
    
    final_return_newPost = SendDateTOnewPost(ref)
        
    return jsonify({"Ref": data})

@app.route('/', methods=['POST'])
def example_endpoint():
    if request.method == 'POST':
        data = request.json 
        print(data)
        datas = CretionNewDate(data)

        return 'POST request successful'
    else:
        return 'Only POST requests are allowed for this endpoint'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
