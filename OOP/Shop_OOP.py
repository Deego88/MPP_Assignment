# Student:Richard Deegan
# Student NUmber: G00387896

# Import libraries
import os
import csv


#****** CREATE DATA CLASS******#
# Create a data class for Product
class Product:

    def __init__(self, name, price=0):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product: {self.name}; \tPrice: {self.price:.2f}"

# Create a data class for ProductStock


class Product_stock:

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    # method to allow self as instance of the class
    def name(self):
        return self.product.name

    def unit_price(self):
        return self.product.price

    def cost(self):
        return self.unit_price() * self.quantity

    def __repr__(self):
        # self.product below is an instance of a class
        return f"{self.product} \tAvailable amount: {self.quantity:.0f}"

# Create a data class for Customer


class Customer:

    def __init__(self, path):
        self.shopping_list = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.name = first_row[0]
            self.budget = float(first_row[1])
            for row in csv_reader:
                name = row[0]
                quantity = float(row[1])
                p = Product(name)
                ps = Product_stock(p, quantity)
                self.shopping_list.append(ps)

    def get_costs(self, price_list):
        total_cost = 0
        for list_item in self.shopping_list:
            for shop_item in price_list:
                if (list_item.name() == shop_item.name()):  # the product is in stock
                    list_item.product.price = shop_item.unit_price()
                    sub_total = list_item.quantity * list_item.product.price
                    total_cost = + sub_total
                    return print(
                        f"(test: {list_item.name()}) OK, there is enough of the product and sub-total would be €{sub_total}")
                else:
                    # print("not in stock, aaaa")
                    pass

    def check_quantity(self, stock_list):
        pass

    def order_cost(self):
        cost = 0

        for list_item in self.shopping_list:
            cost += list_item.cost()

        return cost

    # Customer's shopping list

    def evaluate_order(self, sh):

        # Show customers details
        print("*****************************************")
        print(
            f"\nThe customer name is: {self.name}, the customer budget is: €{self.budget:.2f}")
        print("*****************************************")

        print(f"{self.name} wants the following products: ")

        # initialise
        self.total_cost = 0
        self.total_order_list = []

        # Create a for loop to loop over shopping list
        for cust_item in self.shopping_list:
            # Show customers details
            print(
                f" -{cust_item.product.name}, quantity {cust_item.quantity:.0f}. ", end="")

            # initialise
            sub_total = 0

            # control the messages about the customer
            customer_stock_state = 0  # stock check

            # loop over the stock list to find a match
            for shop_item in sh.stock:

                # check if match exists
                if (cust_item.name() == shop_item.name()) and (cust_item.quantity <= shop_item.quantity):

                    # get the product price form shop
                    cust_item.product.price = shop_item.unit_price()
                    sub_total_full = cust_item.quantity * cust_item.product.price

                    # update total cost
                    sub_total = + sub_total_full

                    # update list of items that are making it for purchasing
                    n = cust_item.name()  # product name variable
                    q = cust_item.quantity  # product quantity variable
                    p = Product(n)  # new instance of class
                    sub_order = Product_stock(p, q)  # a new instance
                    self.total_order_list.append(
                        sub_order)  # append the item

                    # stock check
                    customer_stock_state = 1

                # not enough stock for customer roder
                elif (cust_item.name() == shop_item.name()) and (cust_item.quantity > shop_item.quantity):

                    # check how many can be bought
                    partial_order_qty = cust_item.quantity - \
                        (cust_item.quantity -
                         shop_item.quantity)  # purchase all stock

                    # Cost of the (i-th) item from the customer's shopping list
                    sub_total_partial = partial_order_qty * \
                        shop_item.product.price

                    # update total cost
                    sub_total = + sub_total_partial

                    # as above
                    n = cust_item.name()
                    q = partial_order_qty
                    p = Product(n)
                    sub_order = Product_stock(p, q)
                    self.total_order_list.append(
                        sub_order)  # append

                    # stock check
                    customer_stock_state = 2

                # none in stock
                elif ((cust_item.name() == shop_item.name()) and (shop_item.quantity <= 0)):
                    # Prints out cost of all items of the product
                    customer_stock_state = 0  # none in stock

                # else:
                    # customer_stock_state = 0  # none in stock

            # addition of sub totals
            self.total_cost = self.total_cost + sub_total

            if customer_stock_state == 1:
                # stock check - all quantity can satisfied
                print(
                    f"\tThe shop has stock and sub-total cost would be €{sub_total_full:.2f}")
            elif customer_stock_state == 2:
                # stock check - partial quantity can satisfied
                print(
                    f"\Sorry only {partial_order_qty:.0f} is available and sub-total cost for that many would be €{sub_total_partial:.2f}.")
            elif customer_stock_state == 0:
                # stock check - item not available
                print(
                    f"\tThis product is not available. Sub-total cost will be €{sub_total:.2f}.")

        print(
            f"\nTotal shopping cost will be: €{self.total_cost:.2f}. \n")

        self.total_cost
        self.total_order_list

    def __repr__(self):

        for item in self.shopping_list:
            cost = item.cost()
            str += f"\n{item}"
            if (cost == 0):
                str += f" {self.name} doesn't know how much that costs :("
            else:
                str += f" COST: {cost:.2f}"

        str += f"\nThe cost would be: {self.order_cost():.2f}, he would have {self.budget - self.order_cost():.2f} left"

        return str


#****** SHOP_DETAILS ******#
class Shop:

    def __init__(self, path):
        self.stock = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            self.cash = float(first_row[0])
            for row in csv_reader:
                p = Product(row[0], float(row[1]))
                ps = Product_stock(p, float(row[2]))
                self.stock.append(ps)

#****** SHOP_DETAILS_ORDER ******#
    def process_order(self, cust, sh, total_cost, total_order_list):

        # Check whether the customer can afford the desired items
        if (cust.budget < total_cost):  # customer is short of money
            print(
                f"Sorry, you do not have enough funds, you require €{(total_cost - cust.budget):.2f}. ", end="")
        # else customer has enough money
        else:

            # loop over the items in the customer shopping list
            for cust_item in cust.total_order_list:
             # Initialise (no match=0)
                match_exist = 0
             # Assign the (i-th) product from the customer schopping list as a shorthand
                cust_item_name = cust_item.product.name

               # loop over the stock list to find a match
                for sh_item in sh.stock:
                    # assign the (j-th) product from the shop stock list as a shorthand
                    sh_item_name = sh_item.product.name
                    # check if there is a match
                    if (cust_item_name == sh_item_name):
                        match_exist = + 1

                        # IF sufficient amount exists do the following
                        if (cust_item.quantity <= sh_item.quantity):
                            # update the shop stock
                            sh_item.quantity = sh_item.quantity - cust_item.quantity
                            print(
                                f"Stock quantity of {cust_item.product.name} updated to: {sh_item.quantity:.0f}")

                        else:  # customer wants more than in stock
                            # buy whole stock of the current item
                            partial_order_qty = cust_item.quantity - \
                                (cust_item.quantity - sh_item.quantity)

                            # update the shop stock
                            sh_item.quantity = sh_item.quantity - partial_order_qty

                            print(
                                f"Shop product {cust_item.product.name} is now updated to {sh_item.quantity:.0f}.")

                # IF product is not in the shop, there is no match
                if (match_exist == 0):
                    print(
                        f"\tSorry the shop doesn't have this product.")

            # update shop and customer
            sh.cash = sh.cash + total_cost

            cust.budget = cust.budget - total_cost

            print(f"\nShop has now €{sh.cash:.2f} in cash. ")
            # updated customer's budget
            print(f"{cust.name}'s remaining money is €{cust.budget:.2f}.")
            print("")

        return

# ****** LIVE_MODE ******

    def interactive_mode(self, sh, budget):

        # print  stock
        print(f"\nThis is a list of products for sale in the shop:")
        print(self)

        # initialise
        product_name = ""
        quantity = 0

        # initialise a forever loop forcing the user to exit only with an x
        while product_name != "x":

            print()
            # Request input from the user, assign to the variable
            product_name = input(
                "Please enter your product name (press x to exit): ")

            # initialise (0 = no match)
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

                    quantity = int(
                        input("Please enter your requested quantity: "))

                    # check products availability
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

                            # update the shop cash
                            sh.cash = sh.cash + sub_total
                            print(
                                f"Shop quantity of {sh_item_name} in now: {sh_item.quantity:.0f}. The shop has now: {sh.cash:.2f}.")

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
                            f"Only {partial_order_qty:.0f} is available. Sub-total cost was €{sub_total_partial:.2f}. ")

                        # update customer's budget
                        budget = budget - sub_total_partial
                        print(
                            f"Customer budget is: €{budget:.2f} after buying this item.")

                        # update the shop stock adn cash
                        sh_item.quantity = sh_item.quantity - partial_order_qty

                        sh.cash = sh.cash + sub_total_partial
                        print(
                            f"This product is not avilable in the shop: {sh_item.quantity:.0f}). Cash in shop now: {sh.cash:.2f}.")

            if (match_exist == 0):  # product not available in stock
                print("Product unavailable.")

# ****** SHOP_MENU ******

    def display_menu(self):

        while True:  # this is a 'forever' loop, unless interupted (break)

            # Main menu screen
            print("***************\n")
            print("***************\n")
            print("Welcome to the Shop Main Menu:\n")
            print("***************\n")
            print("1 - Shop Details\n")
            print("2 - Customer A - good case\n")
            print("3 - Customer B - Broke funds case\n")
            print("4 - Customer C - exceeding order case\n")
            print("5 - Live Mode\n")
            print("9 - Exit\n")
            print("NB: The sequence of the customers being processed might affect the initial case of the customers.\n")
            print("***************\n")

            # Request user input
            choice = input("Please enter your choice: ")

            if (choice == "1"):
                print(self)

            elif (choice == "2"):

                # create customer A- good case csv
                customer_A = Customer("../Data/customer_good.csv")

                # print customer details
                customer_A.evaluate_order(self)

                # total_cost = evaluate_order(customer_A, shop)

                # process customer's shopping list by calling relevant method
                self.process_order(customer_A, self,
                                   customer_A.total_cost, customer_A.total_order_list)

            elif (choice == "3"):
                # create customer B- broke case
                customer_B = Customer(
                    "../Data/customer_broke.csv")

                # print customer details and evaluate shopping list
                customer_B.evaluate_order(self)

                # process customer's shopping list by calling relevant method
                self.process_order(customer_B, self,
                                   customer_B.total_cost, customer_B.total_order_list)

            elif (choice == "4"):
                #  create customer C- exceeding case
                # read data from a file
                customer_C = Customer("../Data/customer_exceeding_order.csv")

                # print customer details and evaluate shopping list
                customer_C.evaluate_order(self)

                # process customer's shopping list by calling relevant method
                self.process_order(customer_C, self,
                                   customer_C.total_cost, customer_C.total_order_list)

            elif (choice == "5"):

                # Welcoming message
                print("\You are now in Live Mode")
                print("-------------------------")

                # # get user's name
                self.customer_name = input("Enter your name please: ")
                print(
                    f"Welcome, {self.customer_name} to the live shopping experience. ")

                # get user's budget
                self.budget = float(
                    input("Please tell me your shopping budget: "))

                # go to the interactive mode
                self.interactive_mode(self, self.budget)

            elif (choice == "9"):  # Exit condition
                print("")
                break

#******_ SHOP_SELF******#

    def __repr__(self):
        str = ""
        str += f"\nShop has {self.cash:.2f} in cash \n==== ==== ====\n"
        for item in self.stock:
            str += f"{item}\n"

        return str


def main():

    # Clear screen
    os.system("cls")   # for Windows
    os.system("cls")  # for Linux

    shop_one = Shop("../Data/shop_stock.csv")

    # function that displays the shop menu
    shop_one.display_menu()

    # deafault customer
    c = Customer("../Data/customer.csv")
    c.get_costs(shop_one.stock)
    print(c)


if __name__ == "__main__":
    # execute only if run as a script
    main()
