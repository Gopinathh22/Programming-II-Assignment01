import datetime 
class Coupon:
    def __init__(self, code, discount, validity_date, catagory):
        self.code = code
        self.discount = discount
        self.validity_date = validity_date
        self.catagory = catagory
        self.allCoupons = []
        self.date = datetime.datetime.now()