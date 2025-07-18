import argparse
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.triad_matrix import TriadMatrix
from src.wac_token import WacToken

import pickle

# File paths for persisting state
MATRIX_FILE = "triad_matrix.pkl"
TOKEN_FILE = "wac_token.pkl"

def load_or_create(filename, constructor):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return constructor()

def save_state(matrix, token):
    with open(MATRIX_FILE, 'wb') as f:
        pickle.dump(matrix, f)
    with open(TOKEN_FILE, 'wb') as f:
        pickle.dump(token, f)

def main():
    parser = argparse.ArgumentParser(description="SeirChain CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # 'balance' command
    balance_parser = subparsers.add_parser("balance", help="Check the balance of an address")
    balance_parser.add_argument("address", help="The address to check")

    # 'total_staked' command
    subparsers.add_parser("total_staked", help="Get the total amount of staked WAC tokens")

    # 'transfer' command
    transfer_parser = subparsers.add_parser("transfer", help="Transfer WAC tokens")
    transfer_parser.add_argument("from_address", help="The sender's address")
    transfer_parser.add_argument("to_address", help="The recipient's address")
    transfer_parser.add_argument("amount", type=int, help="The amount to transfer")

    # 'add_triad' command
    add_triad_parser = subparsers.add_parser("add_triad", help="Add a new triad to the matrix")
    add_triad_parser.add_argument("parent_hash", help="The hash of the parent triad")
    add_triad_parser.add_argument("transactions", nargs="+", help="The transactions to include in the triad")

    # 'get_triad' command
    get_triad_parser = subparsers.add_parser("get_triad", help="Get details of a specific triad")
    get_triad_parser.add_argument("hash", help="The hash of the triad to retrieve")

    # 'stake' command
    stake_parser = subparsers.add_parser("stake", help="Stake WAC tokens")
    stake_parser.add_argument("address", help="The address to stake from")
    stake_parser.add_argument("amount", type=int, help="The amount to stake")

    # 'unstake' command
    unstake_parser = subparsers.add_parser("unstake", help="Unstake WAC tokens")
    unstake_parser.add_argument("address", help="The address to unstake from")
    unstake_parser.add_argument("amount", type=int, help="The amount to unstake")

    # 'create_proposal' command
    proposal_parser = subparsers.add_parser("create_proposal", help="Create a new governance proposal")
    proposal_parser.add_argument("proposal_id", help="The ID of the proposal")
    proposal_parser.add_argument("description", help="The description of the proposal")

    # 'get_proposal' command
    get_proposal_parser = subparsers.add_parser("get_proposal", help="Get details of a specific proposal")
    get_proposal_parser.add_argument("proposal_id", help="The ID of the proposal to retrieve")

    # 'vote' command
    vote_parser = subparsers.add_parser("vote", help="Vote on a governance proposal")
    vote_parser.add_argument("proposal_id", help="The ID of the proposal to vote on")
    vote_parser.add_argument("voter_address", help="The address of the voter")
    vote_parser.add_argument("votes", type=int, help="The number of votes to cast")

    args = parser.parse_args()

    matrix = load_or_create(MATRIX_FILE, TriadMatrix)
    token = load_or_create(TOKEN_FILE, WacToken)

    if args.command == "balance":
        balance = token.get_balance(args.address)
        staked = token.staked_balances.get(args.address, 0)
        print(f"Address: {args.address}")
        print(f"  Balance: {balance} WAC")
        print(f"  Staked:  {staked} WAC")
    elif args.command == "total_staked":
        total_staked = token.get_total_staked()
        print(f"Total Staked: {total_staked} WAC")
    elif args.command == "transfer":
        if token.transfer(args.from_address, args.to_address, args.amount):
            print(f"Successfully transferred {args.amount} WAC from {args.from_address} to {args.to_address}")
            save_state(matrix, token)
        else:
            print("Error: Transfer failed. Insufficient funds.")
    elif args.command == "add_triad":
        try:
            new_triad = matrix.add_triad(transactions=args.transactions, parent_hash=args.parent_hash)
            print("Successfully added new triad:")
            print(f"  Hash: {new_triad.hash}")
            print(f"  Parent Hash: {new_triad.parent_hash}")
            save_state(matrix, token)
        except (ValueError, Exception) as e:
            print(f"Error: {e}")
    elif args.command == "get_triad":
        triad = matrix.get_triad(args.hash)
        if triad:
            print(f"Triad Details (Hash: {triad.hash}):")
            print(f"  Parent Hash: {triad.parent_hash}")
            print(f"  Transactions: {triad.transactions}")
            print(f"  Merkle Root: {triad.merkle_root}")
            print(f"  Coordinates: {triad.coordinates}")
        else:
            print("Error: Triad not found.")
    elif args.command == "stake":
        if token.stake(args.address, args.amount):
            print(f"Successfully staked {args.amount} WAC from {args.address}")
            save_state(matrix, token)
        else:
            print("Error: Staking failed. Insufficient funds or stake exceeds maximum allowed.")
    elif args.command == "unstake":
        if token.unstake(args.address, args.amount):
            print(f"Successfully unstaked {args.amount} WAC from {args.address}")
            save_state(matrix, token)
        else:
            print("Error: Unstaking failed. Insufficient staked balance.")
    elif args.command == "create_proposal":
        if token.create_proposal(args.proposal_id, args.description):
            print(f"Successfully created proposal '{args.proposal_id}'.")
            save_state(matrix, token)
        else:
            print(f"Error: Proposal ID '{args.proposal_id}' already exists.")
    elif args.command == "get_proposal":
        proposal = token.proposals.get(args.proposal_id)
        if proposal:
            print(f"Proposal Details (ID: {args.proposal_id}):")
            print(f"  Description: {proposal['description']}")
            print("  Votes:")
            for voter, votes in proposal['votes'].items():
                print(f"    {voter}: {votes} votes")
        else:
            print("Error: Proposal not found.")
    elif args.command == "vote":
        if token.vote(args.proposal_id, args.voter_address, args.votes):
            print(f"Successfully voted {args.votes} on proposal '{args.proposal_id}'.")
            save_state(matrix, token)
        else:
            print("Error: Voting failed. Proposal not found or insufficient staked balance for quadratic voting cost.")

if __name__ == "__main__":
    main()
