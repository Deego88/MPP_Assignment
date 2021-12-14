// Student:Richard Deegan
// Student Number: G00387896

// for reading in files
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

                        //****** CREATE DATA STRUCTS ******//

// Create struct Product. Use * for dynamic space allocation.  Double float for more precision. 
struct Product
{
  char *name;
  double price;
};

// Create struct ProductStock. linked to the struct "Product".  Integer used for quantity variable. 
struct ProductStock
{
  struct Product product;
  int quantity;
};


// Create struct ProductQuantity. Linked to the struct "Product". Integer used for quantity variable.
struct ProductQuantity
{
  struct Product product; 
  int quantity;    
};


// Create struct Shop. Double float for more precision. Nested: struct "Shop"--> struct "ProductStock"--> struct "Stock". Integer used for index loop variable.
struct Shop
{
  double cash;        
  struct ProductStock stock[20];
  int index;


// Create struct Customer. Use * for dynamic space allocation. Double float for more precision.  Nested struct "ProductQuantity" with array size. Integer used for index loop variable.
struct Customer
{
  char *name;
  double budget;
  struct ProductQuantity shoppingList[10];
  int index;
};


// Printing information for the products using methods:

// printProduct takes struct "Product" as "prod". nill return. 
void printProduct(struct Product prod) 
{
  // if the price is defined then show name and price. Else show the shopping list with only product name
  if (prod.price == 0)
  {
    printf("Product: %s; ", prod.name);
  }
  else
  {
    printf("Product: %s; \tPrice: €%.2f \t", prod.name, prod.price);
}


// Show product_price from another struct
double get_product_price(struct Product prod) 
{
// Values of prod.price from another struct
  return prod.price;

                        //****** CREATE SHOP ******//

// Create and stock the shop. The Struct "Shop" retruns method output createAndStockShop().
struct Shop createAndStockShop() 
{
  // Read in CSV data file  https://stackoverflow.com/questions/3501338/c-read-file-line-by-line/3501681#3501681
  FILE *fp;
  char *line = NULL;
  size_t len = 0;
  size_t read;

  // Read in CSV file
  fp = fopen("../Data/shop_stock.csv", "r"); 

  // Handle errors
  if (fp == NULL)
  {
    printf("File not found\n");
    exit(EXIT_FAILURE);
  }



  // read the first line  https://stackoverflow.com/questions/40066017/how-to-access-the-characters-in-getline-in-c
  read = getline(&line, &len, fp);
  double cashInShop = atof(line);
  // initialise the shop "Shop" struct and save  cash in hand value
  struct Shop shop = {cashInShop};

  // Below we read each line and extract and assign certain data to correct variables.
  // read in each line of the file to != -1 (end of file)
  while ((read = getline(&line, &len, fp)) != -1)
  {
    // printf(": %s \n", line); // This is for testing if the program reads the file

    // Function "strtok" is used to break down the string with a "," https://pubs.opengroup.org/onlinepubs/007904975/functions/strtok.html
    char *nam = strtok(line, ","); // Exctract product name and assigns to variable "name"
    char *pri = strtok(NULL, ","); // Exctract product price 
    char *qua = strtok(NULL, ","); // Exctract product available quantity 

    // Conversion of str adn int: https://www.geeksforgeeks.org/atol-atoll-and-atof-functions-in-c-c/
    double price = atof(pri);
    int quantity = atoi(qua);  
    // product name dynamically alocated memory. limited to 50 char.
    char *name = malloc(sizeof(char) * 50);
    // copies variable 'nam' (initialised in the line above) to string variable 'name'
    strcpy(name, nam);                      

    // assign the read values to the struct placeholders
    struct Product product = {name, price};
    struct ProductStock stockItem = {product, quantity};

    // Data is took form the file and put into the "Shop" struct
    shop.stock[shop.index++] = stockItem; 
    // printf("Product: %s, €%.2f; available: %d pcs.\n", name, price, quantity); // Testing 
  }

  return shop; 
}

                        //****** CUSTOMER SHOP EXPERIENCE******//

// Read in data (product stock) and add to the customer struct
struct Customer create_customer(char *path_to_customer)
{

  // Read in file as previous
  FILE *fp;
  char *line = NULL;
  size_t len = 0;
  size_t read;
  // fiel in same directory, read only
  fp = fopen(path_to_customer, "r");
  //fp = fopen("../Data/customer_broke.csv", "r"); 
  //fp = fopen("../Data/customer_exceeding_order.csv", "r");

  // Error handling in case fiel is not found
  if (fp == NULL)
  {
    printf("File not found\n");
    exit(EXIT_FAILURE);
  }

  // Read the first line- customer name and money
  read = getline(&line, &len, fp);

// Function "strtok" is used to break down the string with a "," https://pubs.opengroup.org/onlinepubs/007904975/functions/strtok.html
  char *nam = strtok(line, ","); // Exctract product name and assigns to variable "name"
  char *bud = strtok(NULL, ","); // Exctract product available quantity 
  
  // Use strcoy to copy "nam" variable to str variable, max length is 50 char for char *name. atof used previously.
  char *name = malloc(sizeof(char) * 50);
  strcpy(name, nam);
  double budget = atof(bud);

  // Assign name and budget moeny to customer
  struct Customer customer = {name, budget};
  //printf("Ccustomer: %s, money: %.2f\n", customer.name, customer.budget); // for testing

// read in each line of the file to != -1 (end of file)
  while ((read = getline(&line, &len, fp)) != -1)
  {
    // Function "strtok" is used to break down the string with a "," https://pubs.opengroup.org/onlinepubs/007904975/functions/strtok.html
    char *p_nam = strtok(line, ","); // Exctract product name 
    char *p_qua = strtok(NULL, ","); // Exctract product available quantity 

    
    // Conversion of str adn int: https://www.geeksforgeeks.org/atol-atoll-and-atof-functions-in-c-c/
    char *name = malloc(sizeof(char) * 50);
    strcpy(name, p_nam);
    int quantity = atoi(p_qua);

    struct Product product = {name};
    // temp variable shopping list item
    struct ProductQuantity shopping_list_item = {product, quantity};
    // printf("Test3: %s, qty: %d\n", shopping_list_item.product, shopping_list_item.quantity); //test Ok
    // Assign shopping_list_items and shoppingList[index] together
    customer.shoppingList[customer.index++] = shopping_list_item;

    // printf("Test2: %s\n", product.name); //test OK
    // printf("Test3: %s\n", price); // test NOT OK
    // printf("qty, %d\n", customer.shoppingList[customer.index]); // for testing - OK
  }
  
  // test
  // printf("Number of itmes: %d\n", customer.index); // test OK
  // printf("1st product: %s\n", customer.shoppingList[0].product.name);       // test OK
  // printf("Amount of 1st product: %d\n", customer.shoppingList[0].quantity); // test OK
  // printf("****\n\n");

  return customer;
}

//****** MAIN MENU ******//

// Method to print out the details of the shop 
void printShop(struct Shop *sh)

// Display details of the shops cash
 printf("\nShop has €%.2f in cash\n", sh->cash);
 printf("==== ==== ====\n");

// For loop to loop over the index and show item details
   for (int i = 0; i < sh->index; i++)
  {
    printProduct(sh->stock[i].product);
    printf("Available amount: %d\n", sh->stock[i].quantity);
  }
  printf("\n");
}


// Method to print out the details of the customer
// Return total cost
double print_customers_details(struct Customer *cust, struct Shop *sh)
{
  // Print customer details as per struct within main method 
  printf("\nCustomer name: %s, budget: €%.2f \n", cust->name, cust->budget); 
  printf("---- ---- ----\n");

  // Initialise variables
  double total_cost = 0.0;

  // int customer_wants = cust.shoppingList[0].quantity;

  // Print the shopping list of the customer
  printf("%s wants the following products: \n", cust->name);

  // For loop to loop over the shopping list of the customer
  for (int i = 0; i < cust->index; i++)
  {
    // Show customers details
    printf(" -%s, quantity %d. ", cust->shoppingList[i].product, cust->shoppingList[i].quantity); // example of chain-accessing the data in the nested stucts

    // Initialise variable
    double sub_total = 0;

    //****** CUSTOMER******//

    // check if shopping list matches shop list of products
    int match_exist = 0;
    // assign product (i-th) name to the shopping list as shorthand
    char *cust_item_name = cust->shoppingList[i].product.name;

    // Loop over the stock to find a match 
    for (int j = 0; j < sh->index; j++)
    {
        // Assign product (j-th) from shop stock list as shorthand
      char *sh_item_name = sh->stock[j].product.name; 

        // Use IF statement and BOOL values to see if we have a match
      if (strcmp(cust_item_name, sh_item_name) == 0)
      {
        match_exist++;

        // Use IF statement to see if we have enough stock in the shop to fulfil the customer order
        // IF enough stock
        if (cust->shoppingList[i].quantity <= sh->stock[j].quantity) 
        {
          printf("\tYes, the shop has enough stock to process your order and "); 

          // Full cost of shopping list (Price* Quantity)
          double sub_total_full = cust->shoppingList[i].quantity * sh->stock[j].product.price;
          printf("you must pay the shop €%.2f. \n", sub_total_full);          
          sub_total = sub_total_full; 
        }

        else 
        {
          // customer wants to order more stockcheck
          // See how many can be bought
          int partial_order_qty = cust->shoppingList[i].quantity - (cust->shoppingList[i].quantity - sh->stock[j].quantity);

          // perform the cost of the i-th item from the customer's shopping list
          double sub_total_partial = partial_order_qty * sh->stock[j].product.price;
          printf("\tThe shop only has %d available in stock and now you must pay the shop €%.2f. \n", partial_order_qty, sub_total_partial); 
          sub_total = sub_total_partial;
        }
        // addition of sub totals
        total_cost = total_cost + sub_total;
      }
    }
    // Product not available, Nill match
    if (match_exist == 0) 
    {
        // Prints out cost of all items of the product
      printf("\tThe product you request is not available. Sorry for the inconvenienceSub-total cost will be €%.2f. \n", sub_total);
    }
  }
  // Print out cost of shopping
  printf("\nthe total scost for todays shopping is €%.2f. \n\n", total_cost); 

  return total_cost;
}



//****** MAIN METHOD ******//

int main()
{

  // Create shop
  struct Shop shop_one = createAndStockShop(); 

  // Nill return
  return 0;
}