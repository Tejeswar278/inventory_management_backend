from mongoengine import *

class Products(EmbeddedDocument):
    name                        = StringField()
    price                       = IntField()
    quantity                    = IntField() 
    description                 = StringField()

    meta                        = {'db_alias': "STORE",}  

class CategoriesProducts(Document):
    name                        = StringField()
    products                    = EmbeddedDocumentListField(Products)

    meta                        = {'db_alias': "STORE",} 

class Cart(Document):
    product_name                = StringField(required=True, unique=True)
    quantity                    = IntField(required=True, default=1)
    price                       = IntField(required=True)
    category_name               = StringField()

    meta                        = {'db_alias': "STORE",}

class Orders(Document):
    order_id                    = StringField(primary_key=True, required=True)
    order_date                  = DateTimeField(required=True)
    products                    = ListField(DictField(), required=True) 
    total_items                 = IntField(required=True)
    total_cart_value            = FloatField(required=True)

    meta                        = {'db_alias': "STORE"}