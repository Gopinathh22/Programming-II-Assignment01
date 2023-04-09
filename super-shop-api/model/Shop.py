import random
import string
import datetime
from collections import Counter

class Shop:
    def __init__(self):
        self.customers = []
        self.products = []
        self.coupon = []

    def addProduct(self, p):
        self.products.append(p)

    def addCustomer(self, c):
        c1 = self.getCustomerbyEmail(c.email)
        if c1 == None:  # customer does not exist with the given email address
            self.customers.append(c)
            return True
        else:
            return False

    def removeCustomer(self, c):
        self.customers.remove(c)

    def getCustomer(self, cust_id):
        for c in self.customers:
            if c.customer_id == cust_id:
                return c

    def getCustomerbyEmail(self, email):
        for c in self.customers:
            if c.email == email:
                return c
            
            
    #-------Here I edited--------#
    def editCustomer(self, c, name, dob, address):
  
        if name == "":
            name = c.name
        else:
            c.name = name
        if dob == "":
            dob = c.dob
        else:
            c.dob = dob
        if address == "":
            address = c.address
        else:
            c.address = address
            
    def temp_pas(self, c):
        password = ''.join(random.choice(string.printable) for i in range(8))
        c.password = password
        return password 
    def reset_pas(self, c, password):
        c.password = password
        return password
    
    def removeProduct(self, p):
        self.products.remove(p)
        
    def getProduct(self, product_id):
        for p in self.products:
            if p.product_id == product_id:
                return p
            
    def updateProduct(self,p,quantity):
        for p in self.products:
            p.quantity += int(quantity)
            return p
        
    def sellProduct(self,p,quantity,c):
        for p in self.products:
            if p.quantity < int(quantity):
                return "Not enough products in stock."
            p.quantity -= int(quantity)
            c.purchases.append(f" {c.name} bought {quantity} {p.name}.")
            return p
        
    def editProduct(self, p, quantity, reason):
        for p in self.products:
            if p.quantity < int(quantity):
                return "Not enough products in stock."
            p.quantity -= int(quantity)
            p.inventoryLog.append(f"{quantity}x {p.name} was removed from inventory because {reason}.")
            return p
        
    def reorderProducts(self):
        products = []
        for p in self.products:
            if p.quantity < 10:
                products.append(p)
        return products
    
    def add2cart(self, c, product_id, quantity):
        for product_id in self.products:
            if product_id.quantity < int(quantity):
                return "Not enough products in stock."
            if int(quantity) == -1:
                for i in range(len(c.cart)):
                    if c.cart[i].find(product_id.name) != -1:
                        product_id.quantity += int(c.cart[i].split()[3])
                        c.cart.pop(i)
                        return "Product removed from cart."
                    else:
                        return "Product not found in cart."
            elif int(quantity) == 0:
                return "Quantity cannot be 0."
            else:    
                product_id.quantity -= int(quantity)
                c.cart.append(f"{quantity} {product_id.name}")
                return f"{c.name} added {quantity} {product_id.name} to cart."
    
    def luhn_checksum(credit_card):  #by: Allwin12 on GitHub
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(credit_card)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10 
    
    def placeOrder(self, c, shipping_address, credit_card):
        orders = []
        if Shop.luhn_checksum(credit_card) != 0:
            return "Invalid credit card."
        if len(c.cart) == 0:
            return "Cart is empty."
        #take item from cart, get quantity, get price, add to total
        total = 0
        for i in range(len(c.cart)):
            for p in self.products:
                if c.cart[i].find(p.name) != -1: 
                    total += p.price * int(c.cart[i].split()[0])
                    orders.append(f"{int(c.cart[i].split()[0])} {p.name}")
                    
        c.cart = []
        if c.bonus_points > 0:
            discount = c.bonus_points * 0.1
            total -= discount
            c.bonus_points = 0
            if total < 0:
                left_over = total * -100
                c.bonus_points = left_over
                total = 0
        new_bonus_points = int(total)
        c.bonus_points += new_bonus_points
        c.bonus_milestone += new_bonus_points
        c.purchases.append(f"{c.name} bought {orders} for {total} and received {new_bonus_points} bonus points. Shipping address: {shipping_address}. Credit card: {credit_card}. Time: {datetime.datetime.now()}. Delivery date: {datetime.datetime.now() + datetime.timedelta(days=3)}")
        #make a list with all items orded and quantity, but split them up
        c.orders.append(orders)
        return f"Order placed. Total: {total} to be shipped to {shipping_address}."
    
    def getOrderHistory(self, c):
        return c.purchases
    def getReturnable(self, c):
        #return products that have been bought in the last 30 days
        returnable_products = []
        for p in self.products:
            for i in range(len(c.purchases)):
                if c.purchases[i].find(p.name) != -1:
                    date = c.purchases[i].split()[-2]
                    date = datetime.datetime.strptime(date, '%Y-%m-%d')
                    if datetime.datetime.now() - date < datetime.timedelta(days=30): 
                        returnable_products.append(c.purchases[i])
        return returnable_products
    
    def getRecommendations(self, c):
        product_quantity = {}
        recommandations = []
        for item in c.orders:
            quantity, product = item.split()
            quantity = int(quantity)
            if product in product_quantity:
                product_quantity[product] += quantity
            else:
                product_quantity[product] = quantity
        top_selling = sorted(product_quantity.items(), key=lambda x: x[1], reverse=True)
        for product, quantity in top_selling:
            recommandations.append(f"{product}: {quantity}")
        return recommandations
    
    def getPoints(self, c):
        return c.bonus_milestone
    
    def addPoints(self, c, points):
        c.bonus_points += int(points)
        return f"{int(points)} points added to {c.name}'s account."
    
    
    def addCoupon(self, new_coupon):
        self.coupon.append(new_coupon)

    
    def validCoupon(self):
        valid_coupons = []
        for coupon in self.coupon:
            #turn string into datetime object
            if coupon.validity_date > datetime.datetime.now():
                valid_coupons.append(coupon)
        return valid_coupons