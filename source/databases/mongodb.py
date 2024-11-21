from mongoengine import *

class Products(EmbeddedDocument):
    name                        = StringField()
    price                       = IntField()
    quantity                    = IntField() 
    description                 = StringField()

    meta                        = {'db_alias': "TICKET",}  

class CategoriesProducts(Document):
    name                        = StringField()
    products                    = EmbeddedDocumentListField(Products)

    meta                        = {'db_alias': "TICKET",}  

