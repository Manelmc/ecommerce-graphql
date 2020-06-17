from datetime import datetime
from random import randint

from graphene import ObjectType,\
    String, List, Int, Field, Mutation, Boolean
from graphene.types.datetime import Date
from graphql import GraphQLError

PRODUCT = {
    "p01": {
        "description": "Nike Shoes"
    },
    "p02": {
        "description": "Addidas Jacket"
    }
}

ITEM = {
    "i01" : {
        "product": "p01",
        "price": "2000",
        "date": datetime(2020, 6, 17)
    },
    "i02" : {
        "product": "p02",
        "price": "500",
        "date": datetime(2020, 6, 1)
    }
}

MERCHANT = {
    "m01": {
        "name": "El Bazar",
        "items": ["i01", "i02"]
    }
}


class Product(ObjectType):
    key = String(required=True)
    description = String()

    def resolve_key(self, info):
        if self.key not in PRODUCT:
            return GraphQLError("The product %s doesn't exist" % self.key)
        return self.key

    def resolve_description(self, info):
        # In the resolver you should fetch the database
        return PRODUCT[self.key]["description"]


class Item(ObjectType):
    key = String(required=True)
    product = Field(Product)
    upload_date = Date()
    current_price = Int()

    def resolve_key(self, info):
        if self.key not in ITEM:
            return GraphQLError("The item %s doesn't exist" % self.key)
        return self.key

    def resolve_current_price(self, info):
        return ITEM[self.key]["price"]

    def resolve_upload_date(self, info):
        return ITEM[self.key]["date"]

    def resolve_product(self, info):
        return Product(key=ITEM[self.key]["product"])


class Merchant(ObjectType):
    key = String(required=True)
    name = String()
    items = List(Item)

    def resolve_key(self, info):
        if self.key not in MERCHANT:
            return GraphQLError("The merchant %s doesn't exist" % self.key)
        return self.key

    def resolve_name(self, info):
        return MERCHANT[self.key]["name"]

    def resolve_items(self, info):
        return [Item(key=p_code) for p_code in MERCHANT[self.key]["items"]]


class CreateProduct(Mutation):
    class Arguments:
        description = String()

    ok = Boolean()
    product = Field(Product)

    @staticmethod
    def generate_product_id():
        new_id = randint(1, 100)
        return "p%s" % new_id

    def mutate(self, info, description):
        new_id = self.generate_product_id()
        PRODUCT[new_id] = {"description": description}
        product = Product(key=new_id)
        ok = True
        return CreateProduct(product=product, ok=ok)
