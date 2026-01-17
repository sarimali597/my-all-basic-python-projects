price=float(input("Enter the price of per item you have purchased: "))
quantity=int(input("Enter the quantity of items you have purchased: "))
discount=float(input("Enter the percentage of discount if not enter 0: "))
total=price*quantity
total_discount=(total*discount)/100
final_bill=total-total_discount
print(f"you have purchaced an item with price {price} and at the quantity {quantity}. \n its total bill is {total}.\n while after {discount} % of discount which is rs {total_discount}\n it becomed total {final_bill}.")
