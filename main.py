import argparse

from flask import Flask
from flask_graphql import GraphQLView
from graphene import ObjectType, Schema, Field, String

from ecommerce_objects import Merchant, Item, Product, CreateProduct

app = Flask(__name__)


class Query(ObjectType):

    item = Field(
        Item, key=String(required=True)
    )
    merchant = Field(
        Merchant, key=String(required=True)
    )
    product = Field(
        Product, key=String(required=True)
    )

    def resolve_item(self, info, key):
        return Item(key=key)

    def resolve_merchant(self, info, key):
        return Merchant(key=key)

    def resolve_product(self, info, key):
        return Product(key=key)


class Mutation(ObjectType):
    create_product = CreateProduct.Field()


schema = Schema(query=Query, mutation=Mutation, auto_camelcase=True)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # GraphiQL interface
    )
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", type=str, default=None)
    parser.add_argument(
        "--port", type=int, default=5000)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=True)
