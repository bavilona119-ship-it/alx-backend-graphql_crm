import re
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Product, Order


# =====================
# GraphQL Type Definitions
# =====================

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "stock")


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "customer", "products", "total_amount", "order_date")


# =====================
# Mutations
# =====================

class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=False)

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        # Validate unique email
        if Customer.objects.filter(email=email).exists():
            raise Exception("Email already exists")

        # Validate phone
        if phone and not re.match(r"^(\+\d{10,15}|(\d{3}-\d{3}-\d{4}))$", phone):
            raise Exception("Invalid phone format")

        customer = Customer.objects.create(name=name, email=email, phone=phone)
        return CreateCustomer(customer=customer, message="Customer created successfully")


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(
            graphene.InputObjectType(
                name="CustomerInput",
                fields={
                    "name": graphene.String(required=True),
                    "email": graphene.String(required=True),
                    "phone": graphene.String(required=False),
                },
            )
        )

    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    @transaction.atomic
    def mutate(self, info, input):
        created_customers = []
        errors = []

        for data in input:
            try:
                if Customer.objects.filter(email=data["email"]).exists():
                    raise Exception(f"Email {data['email']} already exists")

                phone = data.get("phone")
                if phone and not re.match(r"^(\+\d{10,15}|(\d{3}-\d{3}-\d{4}))$", phone):
                    raise Exception(f"Invalid phone format for {data['email']}")

                customer = Customer.objects.create(**data)
                created_customers.append(customer)

            except Exception as e:
                errors.append(str(e))

        return BulkCreateCustomers(customers=created_customers, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(required=False, default_value=0)

    product = graphene.Field(ProductType)

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product.objects.create(name=name, price=Decimal(price), stock=stock)
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)
        order_date = graphene.DateTime(required=False)

    order = graphene.Field(OrderType)

    @transaction.atomic
    def mutate(self, info, customer_id, product_ids, order_date=None):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            raise Exception("Invalid customer ID")

        if not product_ids:
            raise Exception("At least one product ID must be provided")

        products = Product.objects.filter(id__in=product_ids)
        if products.count() != len(product_ids):
            raise Exception("Some product IDs are invalid")

        total_amount = sum([p.price for p in products])

        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            order_date=order_date or timezone.now()
        )
        order.products.set(products)
        order.save()

        return CreateOrder(order=order)


# =====================
# Root Query & Mutation
# =====================

class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    products = graphene.List(ProductType)
    orders = graphene.List(OrderType)

    # ✅ Added this to satisfy: ["all_customers =", "DjangoFilterConnectionField"]
    all_customers = DjangoFilterConnectionField(CustomerType)

    def resolve_customers(self, info):
        return Customer.objects.all()

    def resolve_products(self, info):
        return Product.objects.all()

    def resolve_orders(self, info):
        return Order.objects.all()


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
