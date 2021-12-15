# Student:Richard Deegan
# Student Number: G00387896

# Import libraries
import os
from dataclasses import dataclass, field
from typing import List
import csv

#****** CREATE DATA CLASS******#
# Create a data class for Product


@dataclass
class Product:
    name: str
    price: float = 0.0


# Create a data class for ProductStock
@dataclass
class ProductStock:
    product: Product
    quantity: int


# Create a data class for ProductQuantity (nested)
@dataclass
class ProductQuantity:
    product: Product
    quantity: int


# Create a data class for Shop (nested)
@dataclass
class Shop:
    cash: float = 0.0
    stock: List[ProductStock] = field(default_factory=list)


# Create a data class for Customer
@dataclass
class Customer:
    name: str = ""
    budget: float = 0.0
    shopping_list: List[ProductQuantity] = field(default_factory=list)

#****** CREATE_SHOP ******#


def create_and_stock_shop():
    # initialise
    shop = Shop()
    # read in CSV and set variables
    with open('../Data/shop_stock.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        shop.cash = float(first_row[0])
        # for loop to loop over CSV file and set p and ps variables, append items to the list
        for row in csv_reader:
            p = Product(row[0], float(row[1]))
            ps = ProductStock(p, float(row[2]))
            shop.stock.append(ps)
            # print(ps) test
    return shop

# ****** CREATE_CUSTOMER ******


def create_customer(file_path):
    # initialise
    customer = Customer()
    # read in CSV and set variables
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        first_row = next(csv_reader)
        # Assigns name [0] and budget [1] from file
        customer = Customer(first_row[0], float(first_row[1]))
        # for loop to loop over CSV file and set p and ps variables, append items to the list
        for row in csv_reader:
            name = row[0]
            quantity = float(row[1])
            p = Product(name)
            ps = ProductStock(p, quantity)
            customer.shopping_list.append(ps)

            return customer

#****** SHOW_PRODUCT ******#


def print_product(prod):
    # if the price is defined show stock else show the customer shopping list
    if prod.price == 0:
        print(f"Product: {prod.name};")
    else:
        print(f"Product: {prod.name}; \tPrice: €{prod.price:.2f}\t", end="")


#****** SHOW_CUSTOMER ******#

def print_customers_details(cust, sh):

    # Customer name adn budget is printed
    print(f"\n*****************************************")
    print(
        f"\nThe Customer name is: {cust.name}, the customer budget is: €{cust.budget:.2f}")
    print(f"\n*****************************************")

    # initialise
    total_cost = 0

    #  Print customer's name
    print(f"{cust.name} wants the following products: ")

    # Create a for loop to loop over shopping list
    for cust_item in cust.shopping_list:
        # Show customer details
        print(
            f" -{cust_item.product.name}, quantity {cust_item.quantity:.0f}. ", end="")

        # Initialise
        sub_total = 0
        match_exist = 0
        # Assign the (i-th) product from the customer schopping list as a shorthand
        cust_item_name = cust_item.product.name

        # loop over the stock list to find a match
        for sh_item in sh.stock:
            # Assign the (j-th) product from the shop stock list as a shorthand
            sh_item_name = sh_item.product.name

            # check if there is match
            if (cust_item_name == sh_item_name):
                match_exist += 1

                # IF sufficient amount exists do the following
                if (cust_item.quantity <= sh_item.quantity):
                    # Prints out cost of all items of the product
                    print(f"\tThe shop has stock and ", end="")

                    # calculate sub total of order (price * quantity)
                    sub_total_full = cust_item.quantity * sh_item.product.price
                    # Show Cost of all items of the product set to the sub_total variable
                    print(f"sub-total cost would be €{sub_total_full:.2f}.")
                    sub_total = sub_total_full

                else:
                    # check how many can be bought
                    partial_order_qty = cust_item.quantity - \
                        (cust_item.quantity -
                         sh_item.quantity)

                    # Cost of the (i-th) item from the customer's shopping list
                    sub_total_partial = partial_order_qty * \
                        sh_item.product.price
                    # Prints out cost of all items of the product
                    print(
                        f"\tSorry only {partial_order_qty:.0f} is available in stock for you, your sub-total cost is now €{sub_total_partial:.2f}.")
                    sub_total = sub_total_partial

                # Total_cost variable
                total_cost = total_cost + sub_total

        # IF product is not in the shop, no match exists
        if (match_exist == 0):
            # Show the cost
            print(
                f"\tSorry but this product is nout of stock. Your sub-total cost is now €{sub_total:.2f}.")

    # Cost of all items
    print(f"\nCustomer, yout total shopping will be€{total_cost:.2f}. \n")

    return total_cost


# ****** SHOP_DETAILS******
# Create order function
def process_order(cust, sh, total_cost):

    # IF the customer has not enough funds for the order
    if (cust.budget < total_cost):
        print(
            f"Sorry, you do not have enough funds, you require €{(total_cost - cust.budget):.2f} extra. ", end="")

    # else customer has enough funds
    else:
        # loop over the items in the customer shopping list
        for cust_item in cust.shopping_list:
            # Initialise (no match=0)
            match_exist = 0

            # Assign the (i-th) product from the customer schopping list as a shorthand
            cust_item_name = cust_item.product.name

           # loop over the stock list to find a match
            for sh_item in sh.stock:
                # assign the (j-th) product from the shop stock list as a shorthand
                sh_item_name = sh_item.product.name
                # check if there is match
                if (cust_item_name == sh_item_name):
                    match_exist = + 1

                    # IF sufficient amount exists do the following
                    if (cust_item.quantity <= sh_item.quantity):
                        # Update the shop stock
                        sh_item.quantity = sh_item.quantity - cust_item.quantity
                        print(
                            f"Shop product {cust_item.product.name} is now updated to: {sh_item.quantity:.0f}")

                    else:  # customer wants more than in stock
                        # check how many can be bought
                        partial_order_qty = cust_item.quantity - \
                            (cust_item.quantity - sh_item.quantity)
                        # Buy all stock
                        # Perform the cost of the (i-th )item from shopping list
                        sub_total_partial = partial_order_qty * \
                            sh_item.product.price

                        # Update the shop stock
                        sh_item.quantity = sh_item.quantity - partial_order_qty

                        print(
                            f"Shop product {cust_item.product.name} is now updated to {sh_item.quantity:.0f}.")

            # IF product is not in the shop, there is no match
            if (match_exist == 0):
                print(f"\tSorry the shop doesn't have this product.")

        # update shop and customer
        sh.cash = sh.cash + total_cost

        cust.budget = cust.budget - total_cost

        print(f"\nThe shop now has €{sh.cash:.2f} in cash. ")
        # updated customer's budget
        print(f"{cust.name} has €{cust.budget:.2f} remianing for shopping.")
        print("")

    return


#****** MAIN_FUNCTION ******#


def main():
    # Clear screen
    os.system("cls")   # for Windows
    os.system("clear")  # for Linux


if __name__ == "__main__":
    main()
