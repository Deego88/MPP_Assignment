// Student:Richard Deegan
// Student Number: G00387896

// for reading in files
#include <stdio.h>
#include <string.h>
#include <stdlib.h>


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
}

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
