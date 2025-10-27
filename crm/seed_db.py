from crm.models import Customer, Product, Order
from django.utils import timezone

def seed():
    Customer.objects.all().delete()
    Product.objects.all().delete()
    Order.objects.all().delete()

    # Create sample customers
    c1 = Customer.objects.create(name="Alice", email="alice@example.com", phone="+1234567890")
    c2 = Customer.objects.create(name="Bob", email="bob@example.com", phone="123-456-7890")

    # Create sample products
    p1 = Product.objects.create(name="Laptop", price=999.99, stock=10)
    p2 = Product.objects.create(name="Phone", price=499.99, stock=20)

    # Create sample order
    order = Order.objects.create(customer=c1, order_date=timezone.now())
    order.products.set([p1, p2])
    order.calculate_total()

    print("✅ Database seeded successfully!")


if __name__ == "__main__":
    seed()
