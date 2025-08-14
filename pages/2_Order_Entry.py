import streamlit as st
import pandas as pd
from datetime import datetime
import json
from db.db_utils import get_menu_items, save_order, generate_order_number
from utils.calculator import calculate_order_total, validate_order, generate_bill_text

st.set_page_config(page_title="Order Entry", page_icon="🛒", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #4A148C, #7B1FA2, #AD1457);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: #FFD700;
        margin-bottom: 2rem;
    }
    
    .order-summary {
        background: linear-gradient(135deg, #4A148C, #6A1B9A);
        padding: 1.5rem;
        border-radius: 10px;
        color: #FFD700;
        margin: 1rem 0;
    }
    
    .menu-item {
        background: linear-gradient(135deg, #6A1B9A, #8E24AA);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: white;
    }
    
    .cart-item {
        background: linear-gradient(135deg, #7B1FA2, #AD1457);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        color: white;
    }
    
    .payment-section {
        background: linear-gradient(135deg, #4A148C, #6A1B9A);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="main-header">
        <h1>🛒 Order Entry System</h1>
        <p>Create and manage customer orders</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if service mode is selected
    if not st.session_state.get('service_mode'):
        st.warning("Please select a service mode (Dine-In or Takeaway) from the main page first.")
        if st.button("🏠 Go to Main Page"):
            st.switch_page("app.py")
        return
    
    # Initialize session state
    if 'current_order' not in st.session_state:
        st.session_state.current_order = []
    if 'customer_info' not in st.session_state:
        st.session_state.customer_info = {}
    
    # Display current service mode
    st.success(f"Current Service Mode: **{st.session_state.service_mode}**")
    
    col1, col2 = st.columns([2, 1])
    
    # Left column - Menu items
    with col1:
        st.markdown("### 📋 Menu Items")
        
        try:
            menu_df = get_menu_items()
            
            if menu_df is None or len(menu_df) == 0:
                st.warning("No menu items available. Please add items in Menu Management.")
                return
            
            # Category filter
            categories = ['All'] + sorted(menu_df['category'].unique().tolist())
            selected_category = st.selectbox("Filter by Category", categories)
            
            # Filter menu items
            if selected_category != 'All':
                filtered_menu = menu_df[menu_df['category'] == selected_category].copy()
            else:
                filtered_menu = menu_df.copy()
            
            # Search functionality
            search_term = st.text_input("🔍 Search items", placeholder="Type to search...")
            if search_term:
                filtered_menu = filtered_menu[
                    filtered_menu['name'].astype(str).str.contains(search_term, case=False, na=False)
                ]
            
            # Display menu items
            if len(filtered_menu) > 0:
                for _, item in filtered_menu.iterrows():
                    st.markdown(f"""
                    <div class="menu-item">
                        <h4>{item['name']}</h4>
                        <p><strong>Category:</strong> {item['category']}</p>
                        <p><strong>Price:</strong> ₹{item['price']:.2f} (+ GST {item['gst_rate']:.1f}%)</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_a, col_b = st.columns([1, 3])
                    
                    with col_a:
                        quantity = st.number_input(
                            "Qty", 
                            min_value=0, 
                            max_value=50, 
                            value=0, 
                            key=f"qty_{item['id']}"
                        )
                    
                    with col_b:
                        if st.button(f"➕ Add to Order", key=f"add_{item['id']}"):
                            if quantity > 0:
                                # Check if item already exists in order
                                existing_item_index = None
                                for idx, order_item in enumerate(st.session_state.current_order):
                                    if int(order_item['id']) == int(item['id']):
                                        existing_item_index = idx
                                        break
                                
                                if existing_item_index is not None:
                                    st.session_state.current_order[existing_item_index]['quantity'] += quantity
                                    st.success(f"Updated {item['name']} quantity to {st.session_state.current_order[existing_item_index]['quantity']}")
                                else:
                                    new_item = {
                                        'id': int(item['id']),
                                        'name': str(item['name']),
                                        'category': str(item['category']),
                                        'price': float(item['price']),
                                        'gst_rate': float(item['gst_rate']),
                                        'quantity': int(quantity)
                                    }
                                    st.session_state.current_order.append(new_item)
                                    st.success(f"Added {quantity} x {item['name']} to order")
                                
                                st.rerun()
                            else:
                                st.warning("Please select a quantity greater than 0")
        
        except Exception as e:
            st.error(f"Error loading menu: {str(e)}")
    
    # Right column - Current order
    with col2:
        st.markdown("### 🛒 Current Order")
        
        if st.session_state.current_order and len(st.session_state.current_order) > 0:
            # Display order items
            for idx, item in enumerate(st.session_state.current_order):
                try:
                    item_name = str(item.get('name', 'Unknown Item'))
                    item_quantity = int(item.get('quantity', 0))
                    item_price = float(item.get('price', 0))
                    
                    st.markdown(f"""
                    <div class="cart-item">
                        <h5>{item_name}</h5>
                        <p>Qty: {item_quantity} x ₹{item_price:.2f}</p>
                        <p><strong>Total: ₹{item_price * item_quantity:.2f}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col_x, col_y = st.columns(2)
                    
                    with col_x:
                        if st.button("🗑️", key=f"remove_{idx}", help="Remove item"):
                            st.session_state.current_order.pop(idx)
                            st.rerun()
                    
                    with col_y:
                        new_qty = st.number_input(
                            "Qty", 
                            min_value=1, 
                            max_value=50, 
                            value=item_quantity, 
                            key=f"update_qty_{idx}"
                        )
                        if new_qty != item_quantity:
                            st.session_state.current_order[idx]['quantity'] = new_qty
                            st.rerun()
                            
                except Exception as e:
                    st.error(f"Error displaying cart item {idx}: {str(e)}")
            
            # Order calculations
            calculations = calculate_order_total(st.session_state.current_order)
            
            st.markdown(f"""
            <div class="order-summary">
                <h4>Order Summary</h4>
                <p>Items: {len(st.session_state.current_order)}</p>
                <p>Subtotal: ₹{calculations['subtotal']:.2f}</p>
                <p>GST (5%): ₹{calculations['gst_amount']:.2f}</p>
                <p><strong>Grand Total: ₹{calculations['grand_total']:.2f}</strong></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Customer information
            st.markdown("### 👤 Customer Information")
            
            customer_name = st.text_input(
                "Customer Name", 
                value=st.session_state.customer_info.get('name', ''),
                placeholder="Enter customer name"
            )
            
            customer_phone = st.text_input(
                "Phone Number", 
                value=st.session_state.customer_info.get('phone', ''),
                placeholder="Enter phone number"
            )
            
            # Table number for dine-in
            table_number = ""
            if st.session_state.service_mode == "Dine-In":
                table_number = st.text_input(
                    "Table Number", 
                    value=st.session_state.customer_info.get('table', ''),
                    placeholder="Enter table number"
                )
            
            # Discount
            discount_percent = st.slider("Discount (%)", 0, 50, 0)
            
            if discount_percent > 0:
                calculations = calculate_order_total(st.session_state.current_order, discount_percent)
                st.info(f"Discount applied: ₹{calculations['discount_amount']:.2f}")
                st.info(f"New Total: ₹{calculations['grand_total']:.2f}")
            
            # Payment section
            st.markdown("""
            <div class="payment-section">
                <h4>💳 Payment Information</h4>
            </div>
            """, unsafe_allow_html=True)
            
            payment_method = st.selectbox(
                "Payment Method", 
                ["Cash", "Card", "UPI", "Net Banking"]
            )
            
            # Process order
            if st.button("🧾 Generate Bill", use_container_width=True, type="primary"):
                # Validate order
                is_valid, message = validate_order(st.session_state.current_order)
                
                if not is_valid:
                    st.error(message)
                    return
                
                try:
                    # Prepare order data
                    order_number = generate_order_number()
                    order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    order_data = {
                        'order_number': order_number,
                        'service_mode': st.session_state.service_mode,
                        'customer_name': customer_name,
                        'customer_phone': customer_phone,
                        'table_number': table_number,
                        'subtotal': calculations['subtotal'],
                        'gst_amount': calculations['gst_amount'],
                        'discount_amount': calculations['discount_amount'],
                        'grand_total': calculations['grand_total'],
                        'payment_method': payment_method,
                        'order_status': 'Completed',
                        'order_date': order_date
                    }
                    
                    # Save to database
                    order_id = save_order(order_data, st.session_state.current_order)
                    
                    # Update customer info in session
                    st.session_state.customer_info = {
                        'name': customer_name,
                        'phone': customer_phone,
                        'table': table_number
                    }
                    
                    # Generate bill text
                    bill_text = generate_bill_text(order_data, st.session_state.current_order, calculations)
                    
                    # Display success and bill
                    st.success(f"Order {order_number} completed successfully!")
                    
                    # Show bill
                    st.markdown("### 🧾 Generated Bill")
                    st.code(bill_text, language="text")
                    
                    # Download bill
                    st.download_button(
                        label="📥 Download Bill",
                        data=bill_text,
                        file_name=f"bill_{order_number}.txt",
                        mime="text/plain"
                    )
                    
                    # Export as JSON
                    order_json = {
                        'order_data': order_data,
                        'order_items': st.session_state.current_order,
                        'calculations': calculations
                    }
                    
                    st.download_button(
                        label="📥 Download as JSON",
                        data=json.dumps(order_json, indent=2),
                        file_name=f"order_{order_number}.json",
                        mime="application/json"
                    )
                    
                    # Clear current order
                    if st.button("🆕 Start New Order"):
                        st.session_state.current_order = []
                        st.session_state.customer_info = {}
                        st.rerun()
                
                except Exception as e:
                    st.error(f"Error processing order: {str(e)}")
        
        else:
            st.info("No items in current order. Add items from the menu.")
            
            # Quick actions for empty cart
            if st.button("🏠 Back to Main Page"):
                st.switch_page("app.py")

if __name__ == "__main__":
    main()
