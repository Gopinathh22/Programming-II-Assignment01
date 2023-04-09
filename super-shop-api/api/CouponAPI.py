from flask import jsonify, request
from flask_restx import Resource, Namespace

from model.Coupon import Coupon
from model.data import my_shop
import datetime


CouponAPI = Namespace('coupon',
                       description='Coupon Management')

@CouponAPI.route('/')
class GeneralCustomerOps(Resource):
    @CouponAPI.doc(description="Get a list of all Coupons",
                   params={'code': 'Coupon code', 'discount': 'Discount amount', 'validity_date': 'Date until validity ends (d.m.Y)', 'catagory': 'Catagory of the coupon'})
    
    def post(self):
        # get the post parameters
        args = request.args
        code = args['code']
        discount = args['discount']
        validity_date = args['validity_date']
        catagory = args['catagory']
        validity_date = datetime.datetime.strptime(validity_date, '%d.%m.%Y')
        new_coupon = Coupon(code, discount, validity_date, catagory)
        my_shop.addCoupon(new_coupon)
        return jsonify("Coupon added")

    @CouponAPI.doc(description="Get a list of all Coupons")
    
    def get(self):
        #checks for if the coupon is valid from the input date
        return jsonify(my_shop.validCoupon())