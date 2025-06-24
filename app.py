from flask import Flask, request, jsonify
import requests

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    data=request.get_json()
    source_currency=data['queryResult']['parameters']['unit-currency']['currency']
    source_amount=data['queryResult']['parameters']['unit-currency']['amount']
    target_currency=data['queryResult']['parameters']['currency-name']
   
    cf=fetch_conversion_factor(source_currency,target_currency)
    final_amount= round(source_amount * cf,2)
    response={
        'fulfillmentText':f"{source_amount} {source_currency} is {final_amount} {target_currency}"
    }
    return jsonify(response)

def fetch_conversion_factor(source,target):
    url=f"https://v6.exchangerate-api.com/v6/280fe2fed34b40067469ce94/latest/{source}"
    response=requests.get(url)
    response=response.json()
    response=response["conversion_rates"][target]
    return response

if __name__== "__main__":
    app.run(debug=True)