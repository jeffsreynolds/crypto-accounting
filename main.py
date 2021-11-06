import pandas
from pandas.core.frame import DataFrame
from purchase import Purchase
from sale import Sale
# from transaction import Transaction


data = pandas.read_csv("Main Portfolio FY17-18.csv")

purchases = []
sales = []

for purchase in data[data['Type'] == 'BUY'].iterrows():
    purchases.append(Purchase(purchase))

for sale in data[data['Type'] == 'SELL'].iterrows():
    sales.append(Sale(sale))
    

for sale in sales:
    sale.match_purchase(purchases)

profit = 0
for sale in [sale for sale in sales if sale.profit > 0 and sale.volume_not_matched == 0]:
    profit += sale.profit

print (profit)

with open("sales.csv", "w") as file:
    file.write(f"{sales[0].description()}\n")
    for sale in sales:
        output = ""
        for field in sale.to_tuple():
            output += f"{field},"
        
        file.write(f"{output[:len(output)-1]}\n")
        
        for purchase in sale.matched_purchases:
            file.write(f",,,,,,,,,,,,,,{purchase[0].id},{purchase[1]}\n")
        
        file.write("\n")


        
    

