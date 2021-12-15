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

# ****** CREATE_CUSTOMER ****** https://github.com/Deego88/MPP_Assignment/blob/master/Data/shop_stock.csv


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


# ****** LIVE_MODE ******
def interactive_mode(sh, budget):
    # Print stock
    print(f"\nTthis is a list of products for sale in the shop:")
    print_shop(sh)

    # initialise
    product_name = ""
    quantity = 0

    # initialise a forever loop forcing the user to exit only with an x
    while product_name != "x":

        print()
        # Request input from the user, assign to the variable
        product_name = input(
            "\nPlease enter your product name (press x to exit): ")

        print(f"Searching for: {product_name}")

        # initialise to 0 no match
        match_exist = 0

        # loop over shop stock list looking for a match from customer's list
        for sh_item in sh.stock:

            # initialise
            sub_total = 0

            # assign the (j-th) product from the shop stock list as a shorthand
            sh_item_name = sh_item.product.name

            # IF there is a match
            if (product_name == sh_item_name):

                match_exist += 1  # set match

                quantity = int(input("Please enter your requested quantity: "))

                # check products availability
                # If there is product in stock
                if (quantity <= sh_item.quantity):

                    # check product price and calculate sub-total cost
                    sub_total = sh_item.product.price * quantity

                    # IF customer has enough funds
                    if (budget >= sub_total):

                        # update customer's funds
                        budget = budget - sub_total
                        print(
                            f"Congrats! you bought the product. Sub total cost was €{sub_total:.2f}. Your funds are now €{budget:.2f}.")

                        # update the shop stock and cash
                        sh_item.quantity = sh_item.quantity - quantity

                        sh.cash = sh.cash + sub_total
                        print(
                            f"Shop quantity of {sh_item_name} in now: {sh_item.quantity:.0f}. The shop has {sh.cash:.2f} cash.")

                    else:  # customer cannot afford all
                        print(
                            f"Sorry you do nto have enough funds, you require €{(sub_total - budget):.2f} extra. ", end="")

                # customer wants more than in stock
                else:
                    # check how many can be bought and buy all that is in stock
                    partial_order_qty = quantity - \
                        (quantity - sh_item.quantity)

                    # perform the sub-total cost for the item
                    sub_total_partial = partial_order_qty * \
                        sh_item.product.price
                    # Prints out cost of all items of the product
                    print(
                        f"Only {partial_order_qty:.0f} is available and that many bought. Sub-total cost was €{sub_total_partial:.2f}. ")

                    # update customer's budget
                    budget = budget - sub_total_partial
                    print(
                        f"Budget after buying this item: €{budget:.2f}.")

                    # update the shop stock(partial order) and cash
                    sh_item.quantity = sh_item.quantity - partial_order_qty

                    # update the shop cash
                    sh.cash = sh.cash + sub_total_partial
                    print(
                        f"This product is no longer avilable in shop (stock: {sh_item.quantity:.0f}). Cash in shop now: {sh.cash:.2f}.")

        if (match_exist == 0):  # product not available in stock
            print("Product not found in shop.")


#****** SHOP_DETAILS******#
def print_shop(sh):  # takes 'shop' dataclass as a parameter
    # Show shop detials
    # print(sh)  # for testing - ok
    print(f"\nShop has {sh.cash:.2f} in cash")
    print("==== ==== ====")
    for item in sh.stock:
        print_product(item.product)
        print(f"Available amount: {item.quantity:.0f}")


# ****** SHOP_MENU ******#
def display_menu():

    print("***************\n")
    print("***************\n")
    print("Shop Main Menu\n:")
    print("***************\n")
    print("1 - Shop Details\n")
    print("2 - Customer A - good case\n")
    print("3 - Customer B - Broke funds case\n")
    print("4 - Customer C - exceeding order case\n")
    print("5 - Live mode\n")
    print("9 - Exit\n")
    print("***************\n")


def shop_menu(shop):

    # Main menu screen
    display_menu()

    while True:  # this is a 'forever' loop, unless interupted (break)

        # Request input from the user, assign to variable choice
        choice = input("Please enter your choice: ")

        if (choice == "1"):
            # print("inside option 1\n") # for testing - ok
            print_shop(shop)
            display_menu()

        elif (choice == "2"):
            # print("inside option 2\n") # for testing - ok

            # create customer A struct (good case)
            customer_A = create_customer(
                "../Data/customer_good.csv")  # read data from a file

            # print customer details and shopping list
            total_cost = print_customers_details(customer_A, shop)

            # show customer's shopping list by calling relevant method
            process_order(customer_A, shop, total_cost)

            display_menu()

        elif (choice == "3"):
            # create customer B struct (good case)
            customer_B = create_customer(
                "../Data/customer_broke.csv")  # read data from a file

            # print customer details and shopping list
            total_cost = print_customers_details(customer_B, shop)

            # show customer's shopping list by calling relevant method
            process_order(customer_B, shop, total_cost)

            display_menu()

        elif (choice == "4"):
            # create customer C struct (good case)
            customer_C = create_customer(
                "../Data/customer_exceeding_order.csv")  # read data from a file

            # print customer details and shopping list
            total_cost = print_customers_details(customer_C, shop)

            # show customer's shopping list by calling relevant method
            process_order(customer_C, shop, total_cost)

            display_menu()

        elif (choice == "5"):

            # Welcoming message
            print("\You are now in Live Mode")
            print("-------------------------")

            # get user's name
            customer_name = input("Enter your name please: ")
            print(
                f"Welcome, {customer_name} to the live shopping experience. ")

            # get user's budget
            budget = float(
                input("Please tell me your shopping budget: "))

            # go to the interactive mode
            interactive_mode(shop, budget)

            display_menu()

        elif (choice == "9"):  # Exit condition
            print("")
            break

        else:
            display_menu()


#****** MAIN_FUNCTION ******#
def main():
    # Clear screen
    os.system("cls")   # for Windows
    os.system("cls")  # for Linux

    shop_one = create_and_stock_shop()

    shop_menu(shop_one)


# only for script execution
if __name__ == "__main__":
    main()
