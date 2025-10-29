# =====================
# New Mutation for Low Stock Products
# =====================

class UpdateLowStockProducts(graphene.Mutation):
    """Mutation to automatically restock products with low stock (<10)."""

    updated_products = graphene.List(ProductType)
    message = graphene.String()

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10  # Simulate restocking
            product.save()
            updated_products.append(product)

        if not updated_products:
            return UpdateLowStockProducts(
                updated_products=[],
                message="No products needed restocking."
            )

        return UpdateLowStockProducts(
            updated_products=updated_products,
            message=f"{len(updated_products)} products restocked successfully."
        )


# =====================
# Root Mutation (add new mutation here)
# =====================

class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

    # ✅ New mutation
    update_low_stock_products = UpdateLowStockProducts.Field()
