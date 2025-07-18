class WacToken:
    def __init__(self, initial_supply=1000000):
        self.total_supply = initial_supply
        self.balances = {"genesis": initial_supply}

    def get_balance(self, address):
        return self.balances.get(address, 0)

    def transfer(self, from_address, to_address, amount):
        if self.get_balance(from_address) >= amount:
            self.balances[from_address] -= amount
            self.balances[to_address] = self.get_balance(to_address) + amount
            return True
        return False

    def mint(self, address, amount):
        self.total_supply += amount
        self.balances[address] = self.get_balance(address) + amount
