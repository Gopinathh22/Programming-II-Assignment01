from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Customer import Customer
from model.data import my_shop

CustomerAPI = Namespace('customer',
                        description='Customer Management')


@CustomerAPI.route('/')
class GeneralCustomerOps(Resource):

    @CustomerAPI.doc(description="Get a list of all customers")
    def get(self):
        return jsonify(my_shop.customers)

    @CustomerAPI.doc(
        description="Register a new customer",
        params={'address': 'Customers address',
                'name': 'Customers name',
                'email': 'Customer Email',
                'dob': 'Customer birthday'})
    def post(self):
        # get the post parameters
        args = request.args
        name = args['name']
        email = args['email']
        address = args['address']
        dob = args['dob']
        new_customer = Customer(name, email, address, dob)
        # add the customer
        if my_shop.addCustomer(new_customer):
            return jsonify(new_customer)
        else:
            return jsonify("Customer with the email address already exists")


@CustomerAPI.route('/<customer_id>')
class SpecificCustomerOps(Resource):
    @CustomerAPI.doc(description="Get data about a particular customer")
    def get(self, customer_id):
        search_result = my_shop.getCustomer(customer_id)
        return jsonify(search_result)  # this is automatically jsonified by flask-restx

    @CustomerAPI.doc(description="Delete an existing customer")
    def delete(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")
        my_shop.removeCustomer(c)
        return jsonify("Customer with ID {cust_id} was removed")

    @CustomerAPI.doc(
        description="Update customer data",
        params={'address': 'Customers address',
                'name': 'Customers name',
                'email': 'Customer Email',
                'dob': 'Customer birthday'})
    def put(self, customer_id):
        #-------Here I edited--------#
        args = request.args
        name = args.get('name', '')
        dob = args.get('dob', '')
        address = args.get('address', '')
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")     

        my_shop.editCustomer(c, name, dob, address)
        return jsonify("Customer with ID {cust_id} was updated")
        
        #-------Here I edited--------#

@CustomerAPI.route('/verify')
class CustomerVerficiation(Resource):
    @CustomerAPI.doc(
        description="Verify customer email address",
        params={'token': 'Verification Token sent by email',
                'email': 'Customer Email'})
    def put(self):
        args = request.args
        token = args['token']
        email = args['email']
        customer = my_shop.getCustomerbyEmail(email)
        if customer is None:
            return jsonify("Customer not found.")
        if customer.verify(token):
            return jsonify("Customer is now verified.")
        else:
            return jsonify("Invalid token.")


@CustomerAPI.route('/<customer_id>/pwreset')
class CustomerPWReset(Resource):
    @CustomerAPI.doc(
        description="Generate a temporary password and send via email.", )
    def post(self, customer_id):
        #-------Here I edited--------#
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")
        password = my_shop.temp_pas(c) #Reason: I want to generate a temporary password.
        return jsonify("Temporary password sent to customer.")
        #-------Here I edited--------#

    @CustomerAPI.doc(
        description="Allow password reset based on the temporary password",
        params={'temp_pw': 'Password sent by email',
                'new_pw': 'New password'})
    def put(self, customer_id):
        #-------Here I edited--------#
        args = request.args
        temp_pw = args['temp_pw']
        new_pw = args['new_pw']

        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")
        if c.password == temp_pw:
            my_shop.reset_pas(c, new_pw)
            return jsonify("Password reset successful.")    
        else:
            return jsonify("Password reset failed.")


@CustomerAPI.route('/<customer_id>/add2cart')
class AddToCart(Resource):
    @CustomerAPI.doc(
        description="Add an item to shopping cart, fields: product-id, quantity. To delete an item from cart, set the quantity to -1.",
        params={'product_id': 'Product ID', 'quantity': 'Quantity'})
    def post(self, customer_id):
        args = request.args
        quantity = args['quantity']
        product_id = args['product_id']
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")
        return jsonify(my_shop.add2cart(c, product_id, quantity))
    
            
@CustomerAPI.route('/<customer_id>/order')
class Order(Resource):
    @CustomerAPI.doc(description ="Place an order",
                     params = {'shipping_address': 'Shipping address', 'credit_card': 'Credit card number'})
    def post(self, customer_id):
        args = request.args
        shipping_address = args['shipping_address']
        credit_card = args['credit_card']
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")
        return jsonify(my_shop.placeOrder(c, shipping_address, credit_card))
            
        
@CustomerAPI.route('/<customer_id>/orders')
class OrderHistory(Resource):
    @CustomerAPI.doc(description="Get order history")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")
        return jsonify(my_shop.getOrderHistory(c))  

@CustomerAPI.route('/<customer_id>/returnable')
class Returnable(Resource):
    @CustomerAPI.doc(description="Get items that can be returned")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")
        return jsonify(my_shop.getReturnable(c))
        
        
@CustomerAPI.route('/<customer_id>/recommendations')
class Recommendations(Resource):
    @CustomerAPI.doc(description="Get recommendations")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")
        return jsonify(my_shop.getRecommendations(c))


@CustomerAPI.route('/<customer_id>/points')
class Points(Resource):
    @CustomerAPI.doc(description="Total bonus points")
    def get(self, customer_id):
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")
        return jsonify(my_shop.getPoints(c))

    @CustomerAPI.doc(description="Add bonus points", params={'points': 'Points to add'})
    def put(self, customer_id):
        args= request.args
        points = args['points']
        c = my_shop.getCustomer(customer_id)
        if not c:
            return jsonify("Customer ID {cust_id} was not found")
        return jsonify(my_shop.addPoints(c,points))