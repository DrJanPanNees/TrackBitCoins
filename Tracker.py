!pip install requests

import requests

def get_transaction(tx_id):
    """Fetch transaction details using Blockstream Esplora API."""
    url = f"https://blockstream.info/api/tx/{tx_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching transaction data: {e}")
        return None

def get_address_transactions(address):
    """Fetch all transactions for a given address."""
    url = f"https://blockstream.info/api/address/{address}/txs"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching address transactions: {e}")
        return None

def analyze_transaction(transaction):
    """Analyze a transaction and print key details."""
    print("\nTransaction Analysis:")
    print(f"Transaction ID: {transaction['txid']}")
    print(f"Block Height: {transaction.get('status', {}).get('block_height', 'Unconfirmed')}")
    print(f"Confirmations: {transaction.get('status', {}).get('confirmed', False)}")
    print(f"Timestamp: {transaction.get('status', {}).get('block_time', 'Unknown')}")
    print(f"Size: {transaction['size']} bytes")
    print(f"Fee: {transaction['fee']} satoshis")

    print("\nInputs:")
    for input_tx in transaction['vin']:
        if input_tx['txid'] == "0000000000000000000000000000000000000000000000000000000000000000":
            print("  - Coinbase Transaction (Mining Reward)")
        else:
            print(f"  - Input TXID: {input_tx['txid']}, VOUT: {input_tx['vout']}")

    print("\nOutputs:")
    for output_tx in transaction['vout']:
        address = output_tx.get('scriptpubkey_address', 'Unknown')
        value = output_tx['value']
        print(f"  - Address: {address}, Value: {value} satoshis")

def track_address(address):
    """Track all transactions for a given address."""
    transactions = get_address_transactions(address)
    if transactions:
        print(f"\nTracking Address: {address}")
        for tx in transactions:
            analyze_transaction(tx)
            print("-" * 50)

# Example Usage
if __name__ == "__main__":
    # Track a specific transaction
    tx_id = "26c29c78877656558e07dc5a0439613064ad7da8876f9b2768eef016565478e7"
    transaction = get_transaction(tx_id)
    if transaction:
        analyze_transaction(transaction)

    # Track all transactions for a specific address
    address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"  # Example address (Satoshi's address)
    track_address(address)
