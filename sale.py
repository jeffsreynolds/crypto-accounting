
from numpy import e


class Sale():
    def __init__(self, transaction) -> None:
        self.id = transaction[0]
        self.date = transaction[1].Date
        self.exchange = transaction[1].Exchange
        self.volume = transaction[1]['Base amount']
        self.base_asset = transaction[1]['Base currency']
        self.price = transaction[1]['Quote amount']
        self.price_currency = transaction[1]['Quote currency']
        self.fee = transaction[1].Fee
        self.fee_currency = transaction[1]['Fee currency']
        self.cost = transaction[1]['Costs/Proceeds']
        self.cost_currency = transaction[1]['Costs/Proceeds currency']
        self.net_worth_on_purchase_date = transaction[1][11]
        self.net_worth_currency = transaction[1]['Worth currency']

        self.volume_not_matched = self.volume
        self.matched_purchases = []

        self.profit = 0
    
    def match_purchase(self, purchases):
        index = 0
        purchases = [purchase for purchase in purchases if purchase.base_asset == self.base_asset]
        while self.volume_not_matched > 0:
            try:
                purchase = purchases[index]
                if purchase.volume_still_held > 0:
                    print(f"Attempting to find match for sale {self.id} with purchase {purchase.id}")
                    amount_sold = purchase.sell(self.volume_not_matched)
                    value_of_amount_sold = self.net_worth_on_purchase_date * (amount_sold / self.volume)
                    cost_of_amount_sold = purchase.net_worth_on_purchase_date * (amount_sold / purchase.volume)
                    self.matched_purchases.append((purchase, amount_sold))
                    self.profit += value_of_amount_sold - cost_of_amount_sold
                    self.volume_not_matched -= amount_sold
                
                index += 1
           
            except IndexError:
                print(f"Could not match purchase for sale {self.id}")
                print(self.to_string())
                return

    def cost_per_unit(self):
        return (self.price + self.fee) / self.volume

    def to_string(self):
        print(f"Purchase ID: {self.id}")
        print(f"Purchase Date: {self.date}")
        print(f"Exchange: {self.exchange}")
        print(f"Volume: {self.volume}")
        print(f"Asset: {self.base_asset}")
        print(f"Price: {self.price} {self.price_currency}")
        print(f"Fee: {self.fee} {self.fee_currency}")
        print(f"Cost: {self.cost} {self.cost_currency}")
        print(f"Net worth on purchase date: {self.net_worth_on_purchase_date} {self.net_worth_currency}")
        print(f"Volume not matched: {self.volume_not_matched}")
        print(f"Profit: {self.profit}")
        print("\n\n")

    def to_tuple(self):
        purchase_ids = ""
        for purchase in self.matched_purchases:
            purchase_ids += f"{purchase[0].id}^"

        return  (
            self.id, self.date, self.exchange,
            self.volume, self.base_asset, self.price,
            self.price_currency, self.fee, self.fee_currency,
            self.cost, self.cost_currency,
            self.net_worth_on_purchase_date, self.net_worth_currency,
            self.volume_not_matched,
            purchase_ids,
            "", "", self.profit
        )

    def get_matched_purchases(self):
        for purchase in self.matched_purchases:
            purchase.to_string()

    def description(self):
        return "id, date, exchange, volume, asset, price, price currency, fee, fee currency, cost, cost currency, net worth on purchase date, net worth currency, volume not matched, matched purchase id, matched amount, profit"