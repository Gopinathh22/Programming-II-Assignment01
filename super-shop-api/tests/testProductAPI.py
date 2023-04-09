# test_with_pytest.py
from _pytest.fixtures import fixture

from model.Product import Product
from model.Shop import Shop
from model.Customer import Customer

@fixture
def exampleProduct1():
    p1 = Product("Bread", "10.10.2021", "Food")
    return p1

def test_product_add(exampleProduct1):
    shop = Shop()
    shop.addProduct(exampleProduct1)
    assert exampleProduct1 in shop.products
    # try adding again
    shop.addProduct(exampleProduct1)
    assert len(shop.products) == 2 #Deepak code -> 2 # but should be added only once
    
def test_product_remove(exampleProduct1):
    shop = Shop()
    shop.addProduct(exampleProduct1)
    shop.removeProduct(exampleProduct1)
    assert exampleProduct1 not in shop.products

def test_product_get(exampleProduct1):
    shop = Shop()
    shop.addProduct(exampleProduct1)
    p1 = shop.getProduct(exampleProduct1.product_id)
    assert p1 == exampleProduct1
    
def test_product_edit(exampleProduct1):
    shop = Shop()
    shop.addProduct(exampleProduct1)

    p1 = shop.editProduct(exampleProduct1, 1, "Expired")
    assert p1.quantity == 11  #self.quantity = 12
    assert p1.inventoryLog == ["1x Bread was removed from inventory because Expired."]

def test_add_to_cart(exampleProduct1):
    shop = Shop()
    shop.addProduct(exampleProduct1)
    c1 = Customer("Markus Muelle", "markus.mueller@email.test", "1101 Vienna", "10.09.2001")
    shop.addCustomer(c1)
    p1 = shop.add2cart(c1, exampleProduct1, 1)
    assert p1 == "Markus Muelle added 1 Bread to cart."
    assert c1.cart == ["1 Bread"]
    assert exampleProduct1.quantity == 11
    
def test_place_order(exampleProduct1):
    shop = Shop()
    shop.addProduct(exampleProduct1)
    c1 = Customer("Markus Muelle", "markus.mueller@email.test", "1101 Vienna", "10.09.2001")
    shop.addCustomer(c1)
    shop.add2cart(c1, exampleProduct1, 1)
    #place an order
    p1 = shop.placeOrder(c1, "1101 Vienna", "4485077429581220")
    #return f"Order placed. Total: {total} to be shipped to {shipping_address}."
    assert p1 == "Order placed. Total: 100 to be shipped to 1101 Vienna."
    assert c1.cart == []
    assert exampleProduct1.quantity == 11
    #assert c1.purchases == ["Markus Muelle bought ['1 Bread'] for 100 and received 100 bonus points. Shipping address: 1101 Vienna. Credit card: 4485077429581220. Time: 2023-04-09 12:46:37.334552. Delivery date: 2023-04-12 12:46:37.334560"] 
    #time is not the same
    

