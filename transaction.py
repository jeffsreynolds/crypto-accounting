import purchase
import sale

class Transaction():
    def __init__(self, base_asset, purchased_with_asset) -> None:
        self.purchases = []
        self.sales = []
        self.base_asset = base_asset
        self.purchased_with_asset = purchased_with_asset
