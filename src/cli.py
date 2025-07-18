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
    add_triad_parser.add_argument("parent_hash", help="The hash of the parent triad")
    add_triad_parser.add_argument("transactions", nargs="+", help="The transactions to include in the triad")

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

    # 'vote' command
    vote_parser = subparsers.add_parser("vote", help="Vote on a governance proposal")
    vote_parser.add_argument("proposal_id", help="The ID of the proposal to vote on")
    vote_parser.add_argument("voter_address", help="The address of the voter")
    vote_parser.add_argument("votes", type=int, help="The number of votes to cast")

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
        try:
            new_triad = matrix.add_triad(transactions=args.transactions, parent_hash=args.parent_hash)
            print(f"Added new triad with hash: {new_triad.hash}")
        except (ValueError, Exception) as e:
            print(f"Error: {e}")
    elif args.command == "stake":
        if token.stake(args.address, args.amount):
            print(f"Staked {args.amount} WAC from {args.address}")
        else:
            print("Staking failed: Insufficient funds")
    elif args.command == "unstake":
        if token.unstake(args.address, args.amount):
            print(f"Unstaked {args.amount} WAC from {args.address}")
        else:
            print("Unstaking failed: Insufficient staked balance")
    elif args.command == "create_proposal":
        if token.create_proposal(args.proposal_id, args.description):
            print(f"Proposal '{args.proposal_id}' created.")
        else:
            print(f"Proposal ID '{args.proposal_id}' already exists.")
    elif args.command == "vote":
        if token.vote(args.proposal_id, args.voter_address, args.votes):
            print(f"Voted {args.votes} on proposal '{args.proposal_id}' from {args.voter_address}")
        else:
            print("Voting failed: Proposal not found or insufficient staked balance for quadratic voting cost.")

if __name__ == "__main__":
    main()
