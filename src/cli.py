import argparse
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.triad_matrix import TriadMatrix
from src.wac_token import WacToken

def main():
    parser = argparse.ArgumentParser(description="SeirChain CLI")
    subparsers = parser.add_subparsers(dest="command")

    # 'balance' command
    balance_parser = subparsers.add_parser("balance", help="Check the balance of an address")
    balance_parser.add_argument("address", help="The address to check")

    # 'transfer' command
    transfer_parser = subparsers.add_parser("transfer", help="Transfer WAC tokens")
    transfer_parser.add_argument("from_address", help="The sender's address")
    transfer_parser.add_argument("to_address", help="The recipient's address")
    transfer_parser.add_argument("amount", type=int, help="The amount to transfer")

    # 'add_triad' command
    add_triad_parser = subparsers.add_parser("add_triad", help="Add a new triad to the matrix")
    add_triad_parser.add_argument("transactions", nargs="+", help="The transactions to include in the triad")

    args = parser.parse_args()

    # For simplicity, we'll use a single instance of the matrix and token for the CLI
    matrix = TriadMatrix()
    token = WacToken()

    if args.command == "balance":
        balance = token.get_balance(args.address)
        print(f"Balance of {args.address}: {balance} WAC")
    elif args.command == "transfer":
        if token.transfer(args.from_address, args.to_address, args.amount):
            print(f"Transferred {args.amount} WAC from {args.from_address} to {args.to_address}")
        else:
            print("Transfer failed: Insufficient funds")
    elif args.command == "add_triad":
        # In a real implementation, new triads would be added through the consensus mechanism
        new_triad = matrix.add_triad(transactions=args.transactions)
        print(f"Added new triad with hash: {new_triad.hash}")

if __name__ == "__main__":
    main()
