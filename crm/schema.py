import graphene
from graphene_django import DjangoObjectType
from crm.models import Product

# Define Product type
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

# Define Mutation for low-stock update
class UpdateLowStockProducts(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    updated_products = graphene.List(ProductType)

    @classmethod
    def mutate(cls, root, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10  # simulate restocking
            product.save()
            updated_products.append(product)

        message = f"{len(updated_products)} products updated successfully."
        return UpdateLowStockProducts(success=True, message=message, updated_products=updated_products)

# Root mutation class
class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

# Root query (you can extend this as needed)
class Query(graphene.ObjectType):
    products = graphene.List(ProductType)

    def resolve_products(root, info):
        return Product.objects.all()

schema = graphene.Schema(query=Query, mutation=Mutation)
