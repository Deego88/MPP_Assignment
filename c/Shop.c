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