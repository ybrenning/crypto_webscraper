from re import sub
from decimal import Decimal


class Crypto:
    # All attributes will be saved as strings, with functions that can return them
    # as decimal numbers for possible functional use
    def __init__(self, placement, name, price, mcap="", supply=""):
        self.placement = placement
        self.name = name
        self.price = price
        self.mcap = mcap
        self.supply = supply

    def get_mcap_dec(self):
        if self.mcap == "":
            return None
        return Decimal(sub(r"[^\d.]", "", self.mcap))

    def get_supply_dec(self):
        if self.supply == "":
            return None
        return Decimal(sub("\D", "", self.supply))
