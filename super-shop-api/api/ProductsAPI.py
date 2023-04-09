from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Customer import Customer
from model.Product import Product
from model.data import my_shop

ProductAPI = Namespace('product',
                       description='Product Management')


@ProductAPI.route('/')
class AddProductA(Resource):
    @ProductAPI.doc(params={'name': 'Product name',
                            'expiry': 'expiry date',
                            'category': 'product category'})
    def post(self):
        # get the post parameters
        args = request.args
        name = args['name']
        expiry = args['expiry']
        category = args['category']

        new_product = Product(name, expiry, category)
        # add the product
        my_shop.addProduct(new_product)
        return jsonify(new_product)
    #-------Here I edited--------#
    def get(self):
        return jsonify(my_shop.products)
    
@ProductAPI.route('/<product_id>')
class ProductSpecialOps(Resource):
    @ProductAPI.doc(description="Delete an existing product",
                    params={'product_id': 'Product ID'})
    def delete(self, product_id):
        c = my_shop.getProduct(product_id)
        for p in my_shop.products:
            if not p:
                return jsonify("Product ID {prod_id} was not found")
            my_shop.removeProduct(p) 
            return jsonify("Product with ID {prod_id} was removed")
    
    @ProductAPI.doc(description="Get data about a particular product",
                    params={'product_id': 'Product ID'})
    def get(self, product_id):
        search_result = my_shop.getProduct(product_id)
        return jsonify(search_result)
    
    
    
    @ProductAPI.doc(description="Update product data",
                    params={'quantity': 'Product quantity'})
    def put(self, product_id):
        args = request.args
        quantity = args['quantity']
        p = my_shop.getProduct(product_id)
        for p in my_shop.products:
            if not p:
                return jsonify("Product ID {prod_id} was not found")
            my_shop.updateProduct(p, quantity)
            return jsonify("Product with ID {prod_id} was updated")
    
@ProductAPI.route('/sell')
class SellProductA(Resource):
    @ProductAPI.doc(description="Sell a product to Customer and update the quantity",
                    params={'product_id': 'Product ID', 'quantity': 'Product quantity', 'customer_id': 'Customer ID'})
    def put(self):
        args = request.args
        product_id = args['product_id']
        quantity = args['quantity']
        customer_id = args['customer_id']
        p = my_shop.getProduct(product_id)
        c = my_shop.getCustomer(customer_id)
        for c in my_shop.customers:
            if not c:
                return jsonify("Customer ID {cust_id} was not found")
            for p in my_shop.products:
                if not p:
                    return jsonify("Product ID {prod_id} was not found")
                my_shop.sellProduct(p, quantity, c)
                return jsonify("Product with ID {prod_id} was sold")
        
        
@ProductAPI.route('/remove')
class RemoveProductA(Resource):
    @ProductAPI.doc(description="Remove product from inventory,update the quantity and state reason of removal",
                    params={'product_id': 'Product ID', 'quantity': 'Product quantity', 'reason': 'Reason of removal'})
    def put(self):
        args = request.args
        product_id = args['product_id']
        quantity = args['quantity']
        reason = args['reason']
        p = my_shop.getProduct(product_id)
        for p in my_shop.products:
            if not p:
                return jsonify("Product ID {prod_id} was not found")
            my_shop.editProduct(p, quantity, reason)
            return jsonify("Product with ID {prod_id} was removed")
    
    
    
@ProductAPI.route('/reorder')
class ReorderProductA(Resource):
    @ProductAPI.doc(description="Display a list of all products, that must be reordered this week")
    def get(self):  
        return jsonify(my_shop.reorderProducts())
    #-------Here I edited--------#

