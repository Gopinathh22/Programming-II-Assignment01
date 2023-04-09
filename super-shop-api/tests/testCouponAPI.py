# test_with_pytest.py
from _pytest.fixtures import fixture

from model.Product import Product
from model.Shop import Shop
from model.Customer import Customer
from model.Coupon import Coupon


@fixture

def exampleCoupon1():
    c1 = Coupon("2023IMC", "10%", "10.10.2021", "Food")
    return c1    

#check coupon code
def test_coupon_code(exampleCoupon1):
    shop = Shop()
    shop.addCoupon(exampleCoupon1)
    assert exampleCoupon1.code == "2023IMC"
    assert exampleCoupon1.discount == "10%"
def test_coupon_date(exampleCoupon1):
    shop = Shop()
    shop.addCoupon(exampleCoupon1)
    assert exampleCoupon1.validity_date == "10.10.2021"
    


    

def test_coupon_catagory(exampleCoupon1):
    shop = Shop()
    shop.addCoupon(exampleCoupon1)
    assert exampleCoupon1.catagory == "Food"
    


def test_coupon_add(exampleCoupon1):
    shop = Shop()
    shop.addCoupon(exampleCoupon1)
    assert exampleCoupon1 in shop.coupon
    # try adding again
    shop.addCoupon(exampleCoupon1)
    assert len(shop.coupon) == 2 
    
#check for valid coupon
def test_coupon_valid(exampleCoupon1):
    shop = Shop()
    shop.addCoupon(exampleCoupon1)
    assert exampleCoupon1.validity_date == "10.10.2021"
    assert exampleCoupon1.catagory == "Food"
    assert exampleCoupon1.discount == "10%"
    assert exampleCoupon1.code == "2023IMC"
    assert exampleCoupon1 in shop.coupon
    assert len(shop.coupon) == 1
    
#test more invalid coupon
def test_coupon_invalid(exampleCoupon1):
    shop = Shop()
    shop.addCoupon(exampleCoupon1)
    assert exampleCoupon1.validity_date == "10.10.2021"
    assert exampleCoupon1.catagory == "Food"
    assert exampleCoupon1.discount == "10%"
    assert exampleCoupon1.code == "2023IMC"
    assert exampleCoupon1 in shop.coupon
    assert len(shop.coupon) == 1
