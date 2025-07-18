class WacToken:
    def __init__(self, initial_supply=1000000, max_stake_percent=0.1):
        self.total_supply = initial_supply
        self.balances = {"genesis": initial_supply}
        self.staked_balances = {}
        self.proposals = {}
        self.max_stake = initial_supply * max_stake_percent

    def get_balance(self, address):
        return self.balances.get(address, 0)

    def get_total_staked(self):
        return sum(self.staked_balances.values())

    def transfer(self, from_address, to_address, amount):
        if self.get_balance(from_address) >= amount:
            self.balances[from_address] -= amount
            self.balances[to_address] = self.get_balance(to_address) + amount
            return True
        return False

    def mint(self, address, amount):
        self.total_supply += amount
        self.balances[address] = self.get_balance(address) + amount

    def stake(self, address, amount):
        current_stake = self.staked_balances.get(address, 0)
        if self.get_balance(address) >= amount and current_stake + amount <= self.max_stake:
            self.balances[address] -= amount
            self.staked_balances[address] = current_stake + amount
            return True
        return False

    def unstake(self, address, amount):
        if self.staked_balances.get(address, 0) >= amount:
            self.staked_balances[address] -= amount
            self.balances[address] = self.get_balance(address) + amount
            return True
        return False

    def create_proposal(self, proposal_id, description):
        if proposal_id not in self.proposals:
            self.proposals[proposal_id] = {"description": description, "votes": {}}
            return True
        return False

    def vote(self, proposal_id, voter_address, votes):
        if proposal_id in self.proposals:
            staked_balance = self.staked_balances.get(voter_address, 0)
            # Quadratic voting: cost of votes is votes^2
            cost = votes**2
            if staked_balance >= cost:
                self.proposals[proposal_id]["votes"][voter_address] = votes
                return True
        return False

    def get_address_from_coordinates(self, coordinates):
        """Generates a token address from triad coordinates."""
        return "wac_" + "_".join(map(str, coordinates))
