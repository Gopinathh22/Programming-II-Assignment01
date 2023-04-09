# test_with_pytest.py
from _pytest.fixtures import fixture

from model.Customer import Customer
from model.Shop import Shop


@fixture
def exampleCustomer1():
    c1 = Customer("Markus Muelle", "markus.mueller@email.test", "1101 Vienna", "10.09.2001")
    return c1

def test_customer_add(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    assert exampleCustomer1 in shop.customers
    # try adding again
    shop.addCustomer(exampleCustomer1)
    assert len(shop.customers) == 1 # should be added only once

def test_customer_remove(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    shop.removeCustomer(exampleCustomer1)
    assert exampleCustomer1 not in shop.customers

def test_customer_get(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    c1 = shop.getCustomer(exampleCustomer1.customer_id)
    assert c1 == exampleCustomer1
    
def test_customer_edit(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    shop.editCustomer(exampleCustomer1, "Markus", "10.09.2001", "1101 Vienna")
    assert exampleCustomer1.name == "Markus"
    assert exampleCustomer1.dob == "10.09.2001"
    assert exampleCustomer1.address == "1101 Vienna"

def test_customer_temp_pas(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    shop.temp_pas(exampleCustomer1)
    assert exampleCustomer1.password != None

def test_customer_reset_pas(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    shop.reset_pas(exampleCustomer1, "1234")
    assert exampleCustomer1.password == "1234"

def test_customer_getbyEmail(exampleCustomer1):
    shop = Shop()
    shop.addCustomer(exampleCustomer1)
    c1 = shop.getCustomerbyEmail(exampleCustomer1.email)
    assert c1 == exampleCustomer1
    
