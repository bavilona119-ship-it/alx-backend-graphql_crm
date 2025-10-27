import graphene
from graphene_django import DjangoObjectType
from .models import Customer, Product, Order
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction


# === Types ===
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = "__all__"


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = "__all__"


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = "__all__"


# === Queries ===
class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)

    def resolve_customers(root, info):
        return Customer.objects.all()

    def resolve_products(root, info):
        return Product.objects.all()

    def resolve_orders(root, info):
        return Order.objects.select_related("customer").prefetch_related("products").all()


# === Mutations ===

# -- CreateCustomer --
class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=False)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    @staticmethod
    def mutate(root, info, name, email, phone=None):
        # Email uniqueness & validation
        try:
            validate_email(email)
        except ValidationError:
            raise Exception("Invalid email format")

        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")

        # Optional phone validation
        if phone and not (phone.startswith("+") or phone.replace("-", "").isdigit()):
            raise Exception("Invalid phone format")

        customer = Customer.objects.create(name=name, email=email, phone=phone)
        return CreateCustomer(customer=customer, message="Customer created successfully!")


# -- BulkCreateCustomers --
class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(
            graphene.JSONString, required=True, description="List of customer objects"
        )

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, input):
        created_customers = []
        errors = []

        with transaction.atomic():
            for data in input:
                try:
                    name = data.get("name")
                    email = data.get("email")
                    phone = data.get("phone")

                    if not name or not email:
                        raise Exception("Name and Email required")

                    validate_email(email)
                    if Customer.objects.filter(email=email).exists():
                        raise Exception(f"Email {email} already exists")

                    customer = Customer.objects.create(name=name, email=email, phone=phone)
                    created_customers.append(customer)
                except Exception as e:
                    errors.append(str(e))
                    continue

        return BulkCreateCustomers(customers=created_customers, errors=errors)


# -- CreateProduct --
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(required=False, default_value=0)

    product = graphene.Field(ProductType)

    @staticmethod
    def mutate(root, info, name, price, stock):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product.objects.create(name=name, price=price, stock=stock)
        return CreateProduct(product=product)


# -- CreateOrder --
class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    order = graphene.Field(OrderType)

    @staticmethod
    def mutate(root, info, customer_id, product_ids):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")

        products = Product.objects.filter(id__in=product_ids)
        if not products.exists():
            raise Exception("No valid products found")

        order = Order.objects.create(customer=customer)
        order.products.set(products)
        order.calculate_total()

        return CreateOrder(order=order)


# === Root Mutation ===
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
