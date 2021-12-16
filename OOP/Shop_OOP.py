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
                    f"\tOK, there is enough in stock and sub-total cost would be €{sub_total_full:.2f}")
            elif customer_stock_state == 2:
                # stock check - partial quantity can satisfied
                print(
                    f"\tHowever only {partial_order_qty:.0f} is available and sub-total cost for that many would be €{sub_total_partial:.2f}.")
            elif customer_stock_state == 0:
                # stock check - item not available
                print(
                    f"\tThis product is not available. Sub-total cost will be €{sub_total:.2f}.")

        print(
            f"\nTotal shopping cost would be: €{self.total_cost:.2f}. \n")

        self.total_cost
        self.total_order_list


def main():

    # Clear screen
    os.system("cls")   # for Windows
    os.system("cls")  # for Linux

    # function that displays the shop menu


if __name__ == "__main__":
    # execute only if run as a script
    main()
