from decimal import Decimal


class Crypto:
    # All attributes except rank will be saved as strings,
    # with functions that can return them as decimal numbers for possible functional use
    def __init__(self, rank: str, name: str, price: str, mcap: str, supply: str) -> None:
        self.rank = rank
        self.name = name
        self.price = price
        self.mcap = mcap
        self.supply = supply

    def get_price(self) -> Decimal:
        return Decimal(self.price)

    def get_mcap_dec(self) -> Decimal:
        return Decimal(self.mcap)

    def get_supply_dec(self) -> Decimal:
        return Decimal(self.supply)
