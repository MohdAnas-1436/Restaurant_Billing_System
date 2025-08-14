def calculate_order_total(order_items, discount_percent=0):
    """Calculate order totals with GST and discount"""
    if not order_items:
        return {
            'subtotal': 0,
            'gst_amount': 0,
            'discount_amount': 0,
            'grand_total': 0
        }
    
    # Calculate subtotal
    subtotal = sum(item['price'] * item['quantity'] for item in order_items)
    
    # Calculate GST (5% standard)
    gst_amount = subtotal * 0.05
    
    # Calculate discount
    discount_amount = subtotal * (discount_percent / 100)
    
    # Calculate grand total
    grand_total = subtotal + gst_amount - discount_amount
    
    return {
        'subtotal': round(subtotal, 2),
        'gst_amount': round(gst_amount, 2),
        'discount_amount': round(discount_amount, 2),
        'grand_total': round(grand_total, 2)
    }

def format_currency(amount):
    """Format amount as currency"""
    return f"₹{amount:.2f}"

def validate_order(order_items):
    """Validate order items"""
    if not order_items:
        return False, "No items in the order"
    
    for item in order_items:
        if item['quantity'] <= 0:
            return False, f"Invalid quantity for {item['name']}"
        if item['price'] <= 0:
            return False, f"Invalid price for {item['name']}"
    
    return True, "Order is valid"

def generate_bill_text(order_data, order_items, calculations):
    """Generate formatted bill text"""
    bill_text = f"""
    ================================================
              ROYAL RESTAURANT
         Premium Dining Experience
    ================================================
    
    Order Number: {order_data['order_number']}
    Service Mode: {order_data['service_mode']}
    Date & Time: {order_data.get('order_date', '')}
    
    Customer: {order_data.get('customer_name', 'Walk-in Customer')}
    Phone: {order_data.get('customer_phone', 'N/A')}
    {f"Table: {order_data.get('table_number', 'N/A')}" if order_data['service_mode'] == 'Dine-In' else ''}
    
    ================================================
                    ORDER DETAILS
    ================================================
    """
    
    for item in order_items:
        total_price = item['price'] * item['quantity']
        bill_text += f"""
    {item['name']}
    Qty: {item['quantity']} x ₹{item['price']:.2f} = ₹{total_price:.2f}
    """
    
    bill_text += f"""
    ================================================
                    PAYMENT SUMMARY
    ================================================
    
    Subtotal:           ₹{calculations['subtotal']:.2f}
    GST (5%):           ₹{calculations['gst_amount']:.2f}
    Discount:          -₹{calculations['discount_amount']:.2f}
    ------------------------------------------------
    GRAND TOTAL:        ₹{calculations['grand_total']:.2f}
    
    Payment Method:     {order_data['payment_method']}
    Status:             {order_data.get('order_status', 'Completed')}
    
    ================================================
          Thank you for dining with us!
         Visit us again for premium experience
    ================================================
    """
    
    return bill_text
