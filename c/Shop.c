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
};

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

                        //****** SHOP_DATA_PROCESSING ******//

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
    // printf("Product: %s, €%.2f; available: %d pcs.\n", name, price, quantity); // TEST 
  }

  return shop; 
}

                        //****** CUSTOMER_DATA_PROCESSING ******//
// Read in data (product stock) and add to the customer struct
struct Customer create_customer(char *path_to_customer)
{

  // Read in file as previous
  FILE *fp;
  char *line = NULL;
  size_t len = 0;
  size_t read;
  // file in same directory, read only
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
  //printf("Ccustomer: %s, money: %.2f\n", customer.name, customer.budget); // TEST

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
    // printf("Test3: %s, qty: %d\n", shopping_list_item.product, shopping_list_item.quantity); // TEST
    // Assign shopping_list_items and shoppingList[index] together
    customer.shoppingList[customer.index++] = shopping_list_item;

    // printf("Test2: %s\n", product.name); // TEST
    // printf("Test3: %s\n", price); // TEST
    // printf("qty, %d\n", customer.shoppingList[customer.index]); // TEST
  }
  
  // test
  // printf("Number of itmes: %d\n", customer.index); // test OK
  // printf("1st product: %s\n", customer.shoppingList[0].product.name);       // test OK
  // printf("Amount of 1st product: %d\n", customer.shoppingList[0].quantity); // test OK
  // printf("****\n\n");

  return customer;
}

                        //****** SHOP_DETAILS ******//
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

                        //****** CUSTOMER_DETAILS ******//
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

            // ****** SHOP_DETAILS ******
void process_order(struct Customer *cust, struct Shop *sh, double *total_cost)
{

  // IF customer has not enough funds
  if (cust->budget < *total_cost)
  {
    printf("Sorry, you do not have enough funds, you require €%.2f extra. ", (*total_cost - cust->budget));
  }

  else // else customer has enough funds
  {

    //loop over the items in the customer shopping listt
    for (int i = 0; i < cust->index; i++)
    {
      int match_exist = 0;                                       // Initialise (no match=0)
      char *cust_item_name = cust->shoppingList[i].product.name; // Assign the (i-th) product from the customer schopping list as a shorthand

      // loop over the stock list to find a match
      for (int j = 0; j < sh->index; j++)
      {
        char *sh_item_name = sh->stock[j].product.name; // assign the (j-th) product from the shop stock list as a shorthand

        if (strcmp(cust_item_name, sh_item_name) == 0) //  check if there is a match
        {
          match_exist++; 

          //check products availability
          if (cust->shoppingList[i].quantity <= sh->stock[j].quantity) // sufficient amount of the product in the shop stock
          {
            // update the shop stock
            sh->stock[j].quantity = sh->stock[j].quantity - cust->shoppingList[i].quantity;
            printf("Stock quantity of %s updated to: %d \n", cust->shoppingList[i].product.name, sh->stock[j].quantity);
          }

          else // customer wants more than in stock
          {
            // check how many can be bought
            int partial_order_qty = cust->shoppingList[i].quantity - (cust->shoppingList[i].quantity - sh->stock[j].quantity); // will buy all that is in stock

            // Perform the cost of the (i-th )item from shopping list
            double sub_total_partial = partial_order_qty * sh->stock[j].product.price; // partial qty * price
            // update the shop stock
            sh->stock[j].quantity = sh->stock[j].quantity - partial_order_qty;

            printf("Stock product %s is now updated to %d. \n", cust->shoppingList[i].product.name, sh->stock[j].quantity);
          }
        }
      }
      // IF product is not in the shop, there is no match
      if (match_exist == 0) 
      {
        printf("\tSorry the shop doesn't have this product \n");
      }
    }

    // update the shop and customer
    sh->cash = sh->cash + *total_cost;
    cust->budget = (cust->budget - *total_cost);

    printf("\nShop now has €%.2f in cash. \n", sh->cash);
    // printf("%s's remaining money is €%.2f. \n", cust->name, cust->budget); //updated customer's budget
    printf("%s's has €%.2f remaining for shopping. \n", cust->name, cust->budget);
    printf("\n");
  };

  return;
}



//****** LIVE_MODE ******

void interactive_mode(struct Shop *sh, double *budget)
{
  //fflush(stdin); // flushes the input string from any left overs from previous inputs

  // printf("Budget: %.2f\n", (*budget)); // for testing - ok

  // print shops stock
  printf("\nThis is a list of products for sale in the shop:\n");

  printShop(&(*sh));

  // declare required variables
  char product_name[100];
  int quantity;

  //  initialise a forever loop forcing the user to exit only with an x
  while (strcmp(&product_name, "x") != 0)
  {

    // get required data from user's input
    printf("\nPlease enter your product name (press x to exit): ");

    fgets(product_name, sizeof product_name, stdin);
    scanf("%[^\n]%*c", product_name);

    printf("Searching for: \"%s\"", product_name);

    // printf("Test 2: Customer budget: %.2f, product: %s\n", (*budget), product_name); // TEST
    // printf("Test 3: Cash in shop: %f\n", *(&sh->cash));                        // TEST
    // printf("Test 4: Product price of index 2: %.2f\n", *(&sh->stock[2].product.price)); TEST 

    // initialise (0 = no match)
    int match_exist = 0;

    // loop over shop stock list looking for a match from customer's list
    for (int j = 0; j < sh->index; j++)
    {

      // initialise
      double sub_total = 0;
      // assign the (j-th) product from the shop stock list as a shorthand
      char *sh_item_name = sh->stock[j].product.name;

      // IF there is a match
      if (strcmp(product_name, sh_item_name) == 0)
      {
        match_exist++; // set match

        printf("\nPlease enter your requested quantity: ");
        scanf("%d", &quantity);

        // check products availability
        if (quantity <= sh->stock[j].quantity) // sufficient amount of the product in the shop stock
        {
          // check product price and calculate sub-total cost
          sub_total = sh->stock[j].product.price * quantity;

          // IF customer has enough funds
          if (*budget >= sub_total)
          {

            // update customer's funds
            *budget = *budget - sub_total;
            printf("Congrats! you bought the product. Sub total cost was €%.2f. Your funds are now €%.2f. \n", sub_total, *budget);

            // update the shop stock and cash
            sh->stock[j].quantity = sh->stock[j].quantity - quantity;
            
            sh->cash = sh->cash + sub_total;
            printf("Shop quantity of %s in now: %d. The shop has %.2f cash. \n", product_name, sh->stock[j].quantity, sh->cash);
          }

          else
          {
            printf("Sorry you do nto have enough funds, you require €%.2f. ", (sub_total - *budget));
          }
        }

        else // customer wants more than in stock
        {
          // check how many can be bought and buy all that is in stock
          int partial_order_qty = quantity - (quantity - sh->stock[j].quantity);

          // perform the sub-total cost for the item
          double sub_total_partial = partial_order_qty * sh->stock[j].product.price;
          printf("Only %d is available. Sub-total cost was €%.2f. ", partial_order_qty, sub_total_partial);

          // update customer's budget
          *budget = *budget - sub_total_partial;
          printf("Customers Budget is: €%.2f after buying the item. \n", *budget);

          // update the shop stock (partial order) and cash
          sh->stock[j].quantity = sh->stock[j].quantity - partial_order_qty;
          // update the shop cash
          sh->cash = sh->cash + sub_total_partial;
          printf("This product is not avilable in shop (stock: %d). Cash in shop now: %.2f. \n", sh->stock[j].quantity, sh->cash);
        }
      }
    }
    if (match_exist == 0) // product not available in stock
    {
      printf("Product not found in shop. \n");
    }
  }
  //;
}

                        //****** SHOP_MENU ******//


// Menu script adapted from https://stackoverflow.com/questions/42430351/simple-menu-in-c 
void shop_menu(struct Shop sh)
{
  char char_choice[2];
  // initialise the variable
  int choice = -1;

  system("cls");   // Windows systems
  system("clear"); // Linux systems
    
  do
  {
    printf("***************\n");
    printf("Welcome to the Shop Main Menu\n");
    printf("***************\n");
    printf("1. Shop Details\n");
    printf("2. Customer A - good case\n");
    printf("3. Customer B - Broke funds case\n");
    printf("4. Customer C - exceeding order case\n");
    printf("5. Live Mode\n");
    printf("9. Exit\n");
    printf("***************\n");
    printf("Please enter your choice:");


    scanf("%s", char_choice);
    choice = atoi(char_choice);

    switch (choice)
    {

                            //****** PRINT 1. SHOP DETAILS ******//
    // Case switch https://www.guru99.com/c-switch-case-statement.html
    case 1:

      printShop(&sh);

      break;

                            //****** PRINT 2. PROCESS_ORDER_GOOD_CASE ******//
    case 2:; // The C language standard only allows statements​ to follow a label. The language does not group declarations in the same category as statements

      // Create customer A struct, the working case
      // Call the method and read data from a file
      struct Customer customer_A = create_customer("../Data/customer_good.csv"); 

      // Print customer details
      double total_cost = print_customers_details(&customer_A, &sh);

      // Show customer's shopping list
      process_order(&customer_A, &sh, &total_cost);

      break;

                           //****** PRINT 3. PROCESS_ORDER_BROKE_CASE ******//
    case 3:;

      // Create customer B struct, the broke case
      // Call the method and read data from a file
      struct Customer customer_B = create_customer("../Data/customer_broke.csv");

      // Print customer details
      total_cost = print_customers_details(&customer_B, &sh);

      // Show customer's shopping list
      process_order(&customer_B, &sh, &total_cost);

      break;

                            //****** PRINT 4. PROCESS_ORDER_EXCEEDING_CASE ******//
    case 4:;

      // Create customer C struct, exceeding case
      // Call the method and read data from a file
      struct Customer customer_C = create_customer("../Data/customer_exceeding_order.csv");

      // Print customer details
      total_cost = print_customers_details(&customer_C, &sh);

      // Show customer's shopping list
      process_order(&customer_C, &sh, &total_cost);

      break;

    case 5:;
      // Welcoming message
      printf("\nYou are now in Live Mode\n");
      printf("-------------------------\n");

      
      printf("Enter your name please: ");
      // declare the variable
      char *customer_name = malloc(sizeof(char) * 50);
      scanf("%s", customer_name);
      printf("Welcome, %s to the Live Mode shopping experience. \n", customer_name);

      // get user input
      printf("Please tell me your shopping your budget: ");
      // declare the variable
      double budget; 
      scanf("%lf", &budget);
      // printf("Confirming entering budget: €%.2f. \n", budget); // TEST
      interactive_mode(&sh, &budget);

      break;

    case 9:;
      // exit
      break;

    default:
      printf("sorry you have entered a wrong key. Enter the option number only.\n");
      break;
    }
  } 
  while (choice != 9);
}


                        //****** MAIN METHOD ******//
int main()
{

  // Create and stock the shop
  struct Shop shop_one = createAndStockShop();
  // Display shop menu

  shop_menu(shop_one);

  // Nill return
  return 0;
}