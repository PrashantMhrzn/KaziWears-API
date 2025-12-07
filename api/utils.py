import random

def generate_random_code():
    possible_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    short_code = ''
    # creating a random 6 character code
    for _ in range(6):
        short_code += random.choice(possible_characters)
    return short_code


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_order_confirmation_email(order, request=None):
    """
    Send order confirmation email to customer
    """
    customer = order.customer
    order_items = order.items.all()
    
    # Prepare context for template
    context = {
        'customer_name': customer.get_full_name() or customer.username,
        'customer_email': customer.email,
        'order_number': order.order_number,
        'order_date': order.order_date.strftime('%B %d, %Y %I:%M %p'),
        'total_amount': order.total_amount,
        'shipping_address': order.shipping_address,
        'payment_method': order.get_payment_method_display(),
        'status': order.get_status_display(),
        'order_items': [
            {
                'product_name': item.product.name,
                'size': item.size,
                'color': item.color,
                'quantity': item.quantity,
                'price': item.price_at_purchase
            }
            for item in order_items
        ],
        'order_link': f'http://localhost:8000/api/orders/{order.id}/' if request else '#',
        'current_year': order.order_date.year,
    }
    
    # Render HTML content
    html_content = render_to_string('emails/order_confirmation.html', context)
    text_content = strip_tags(html_content)  # Strip HTML for plain text version
    
    # Create email
    subject = f"🎉 Your Kazi Wears Order #{order.order_number} is Confirmed!"
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[customer.email],
        cc=[settings.DEFAULT_FROM_EMAIL] if not settings.DEBUG else [],  # CC to admin in production
    )
    
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
        print(f"✅ Order confirmation email sent to {customer.email}")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False