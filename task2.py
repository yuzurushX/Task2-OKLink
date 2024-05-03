import requests
import pprint
import json
from decimal import Decimal
from datetime import datetime
from prettytable import PrettyTable

# Define variables
TOKEN_ADDRESS = "TOKEN_CONTRACT_ADDRESS"  # Replace with token address that you want to research
OK_ACCESS_KEY = "OKLINK_APIKEY"  # Replace with your OKLink access key

# Base URL for OKLink API
BASE_URL = "https://www.oklink.com/api/v5/explorer"

# Function to fetch token information
def token_info():
    url = f"{BASE_URL}/eth/api?module=token&action=tokeninfo&contractaddress={TOKEN_ADDRESS}"
    headers = {"Ok-Access-Key": OK_ACCESS_KEY, "Content-type": "application/json"}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    
    print(f"\n---------------------------------------------------------------[Token Information]---------------------------------------------------------------\n")
    tokenname = data.get("result", {}).get("tokenName")
    symbol = data.get("result", {}).get("symbol")
    website = data.get("result", {}).get("website")
    twitter = data.get("result", {}).get("twitter")
    whitepaper = data.get("result", {}).get("whitepaper")
    # Print website and Twitter URL (if available)
    print(f"Token Name: {tokenname} ({symbol})")
    print(f"Website: {website}")
    print(f"Twitter: {twitter}")
    print(f"Whitepaper: {whitepaper}")

# Function to fetch historical price data
def token_price_data():
    print(f"\n---------------------------------------------------------------[Token Price Data]---------------------------------------------------------------\n")

    url = f"{BASE_URL}/tokenprice/historical?chainId=1&tokenContractAddress={TOKEN_ADDRESS}&limit=200"
    headers = {"Ok-Access-Key": OK_ACCESS_KEY, "Content-type": "application/json"}
    response = requests.get(url, headers=headers)    
    if response.status_code == 200:
        data = response.json().get('data', [])  # Extract 'data' from JSON response, default to empty list if not present
        if data:
            table = PrettyTable(["Price", "Date", "Price Abnormality"])  # Create table with specified column names
            for item in data:
                time_str = datetime.fromtimestamp(int(item['time']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                table.add_row([item['price'], time_str,item['priceAbnormal']])  # Add only 'price' and 'time' to the table
            print(table)
        else:
            print("No data found.")
    else:
        print(f"Error fetching data: {response.status_code}")
    print()  # Add an empty line after the table

# Function to fetch token holding data
def fetch_holding_data():

    url = f"{BASE_URL}/eth/api?module=token&action=tokenholderlist"
    headers = {"Ok-Access-Key": OK_ACCESS_KEY, "Content-type": "application/json"}
    params = {
        "contractaddress": TOKEN_ADDRESS,
        "offset" : 100
    }
    all_holder = []
    current_page = 1
    print(f"\n---------------------------------------------------------------[Token Holder Data)]---------------------------------------------------------------\n")
    while True:
        params['page'] = current_page
        response = requests.get(url, headers=headers, params=params)
        table = PrettyTable(["Rank", "Holder Address", "Quantity", "Proportion"])
        if response.status_code == 200:
            data = response.json().get("result", [])
            if data:
                holders = data[0].get('result', [])
                all_holder.extend(data)
                current_page += 1
                if len(data) < 100:  # Stop if fewer transactions are returned
                    break
            else:
                break  # No more transaction data
        else:
            print(f"Error fetching transactions: {response.status_code}")
            break      
    i=0
    total_quantity = 0
    for item in all_holder:
        quantity = Decimal(item['TokenHolderQuantity'])
        total_quantity += quantity

    for item in all_holder:
        quantity = Decimal(item['TokenHolderQuantity'])
        proportion = (quantity / total_quantity) * 100
        formatted_quantity = quantity / Decimal(10**18)
        table.add_row([i+1, item['TokenHolderAddress'], formatted_quantity, f"{proportion:.18f}%"])
        i=i+1
    print(table)
    print()
    return all_holder

# Function to fetch token liquidity data
def fetch_liquidity_data():
    print("Fetching token liquidity data...")
    url = f"https://www.oklink.com/api/v5/explorer/polygon/api?module=token&action=tokenholderlist&contractaddress={TOKEN_ADDRESS}&page=1&offset=100"
    headers = {"Ok-Access-Key": OK_ACCESS_KEY, "Content-type": "application/json"}
    response = requests.get(url, headers=headers)
    # Process the response data (parse JSON etc.) to get transactions and volume
    # Implement additional logic to assess liquidity
    print(response.json())  # Placeholder for data processing
    print()
    
def fetch_token_tx():
    
    minimum_amount = 500000
    url = f"https://www.oklink.com/api/v5/explorer/token/transaction-list"
    headers = {"Ok-Access-Key": OK_ACCESS_KEY, "Content-type": "application/json"}
    params = {
        'chainShortName': 'eth',
        'tokenContractAddress': TOKEN_ADDRESS,
        'limit': 50, 
        'minAmount': minimum_amount
    }
    all_transfers = []
    current_page = 1
    print(f"---------------------------------------------------------------[Token Large Transactions (Above {minimum_amount})]---------------------------------------------------------------\n")
    while True:
        params['page'] = current_page
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()['data']
            relevant_data = data[0]
            transactions = data[0].get('transactionList', [])
            all_transfers.extend(transactions)
            current_page += 1

            if int(relevant_data['totalPage']) < current_page:  # Check if more pages exist
                break 
        else:
            print(f"Error fetching transfers: {response.status_code}")
            break
    table = PrettyTable(["TX ID", "Time", "Source", "Destination", "Amount"])
    for item in all_transfers:
        time_str = datetime.fromtimestamp(int(item['transactionTime']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        table.add_row([item['txid'], time_str, item['from'], item['to'],item['amount']])    
    print(table)
    return all_transfers

# Main function
def main():
    token_info()
    token_price_data()
    fetch_holding_data()
    fetch_liquidity_data()
    fetch_token_tx()

if __name__ == "__main__":
    main()
