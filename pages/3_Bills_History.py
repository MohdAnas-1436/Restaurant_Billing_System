import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
from db.db_utils import get_orders
from utils.calculator import generate_bill_text

st.set_page_config(page_title="Bills History", page_icon="📄", layout="wide")

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
    
    .bill-card {
        background: linear-gradient(135deg, #6A1B9A, #8E24AA);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
    }
    
    .summary-card {
        background: linear-gradient(135deg, #7B1FA2, #AD1457);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="main-header">
        <h1>📄 Bills History</h1>
        <p>View and manage all billing records</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Date range selector
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_from = st.date_input(
            "From Date",
            value=datetime.now().date() - timedelta(days=30)
        )
    
    with col2:
        date_to = st.date_input(
            "To Date",
            value=datetime.now().date()
        )
    
    with col3:
        if st.button("📊 Load Bills", type="primary"):
            st.session_state.load_bills = True
    
    # Quick date filters
    st.markdown("**Quick Filters:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📅 Today"):
            st.session_state.date_from = datetime.now().date()
            st.session_state.date_to = datetime.now().date()
            st.session_state.load_bills = True
    
    with col2:
        if st.button("📅 Yesterday"):
            yesterday = datetime.now().date() - timedelta(days=1)
            st.session_state.date_from = yesterday
            st.session_state.date_to = yesterday
            st.session_state.load_bills = True
    
    with col3:
        if st.button("📅 This Week"):
            today = datetime.now().date()
            start_week = today - timedelta(days=today.weekday())
            st.session_state.date_from = start_week
            st.session_state.date_to = today
            st.session_state.load_bills = True
    
    with col4:
        if st.button("📅 This Month"):
            today = datetime.now().date()
            start_month = today.replace(day=1)
            st.session_state.date_from = start_month
            st.session_state.date_to = today
            st.session_state.load_bills = True
    
    # Load and display bills
    if st.session_state.get('load_bills') or st.button("🔄 Refresh"):
        try:
            # Get date range
            from_date = st.session_state.get('date_from', date_from)
            to_date = st.session_state.get('date_to', date_to)
            
            # Load orders
            orders_df = get_orders(
                date_from=from_date.strftime('%Y-%m-%d'),
                date_to=to_date.strftime('%Y-%m-%d')
            )
            
            if orders_df.empty:
                st.warning("No bills found for the selected date range.")
                return
            
            # Summary statistics
            st.markdown("### 📊 Summary")
            
            total_orders = len(orders_df)
            total_revenue = orders_df['grand_total'].sum()
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
            total_gst = orders_df['gst_amount'].sum()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="summary-card">
                    <h4>Total Orders</h4>
                    <h2>{total_orders}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="summary-card">
                    <h4>Total Revenue</h4>
                    <h2>₹{total_revenue:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="summary-card">
                    <h4>Avg Order Value</h4>
                    <h2>₹{avg_order_value:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="summary-card">
                    <h4>Total GST</h4>
                    <h2>₹{total_gst:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # Service mode breakdown
            service_breakdown = orders_df['service_mode'].value_counts()
            st.markdown("### 📊 Service Mode Breakdown")
            
            col1, col2 = st.columns(2)
            
            for idx, (mode, count) in enumerate(service_breakdown.items()):
                col = col1 if idx % 2 == 0 else col2
                revenue = orders_df[orders_df['service_mode'] == mode]['grand_total'].sum()
                
                with col:
                    st.markdown(f"""
                    <div class="summary-card">
                        <h4>{mode}</h4>
                        <p>Orders: {count}</p>
                        <p>Revenue: ₹{revenue:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Payment method breakdown
            payment_breakdown = orders_df['payment_method'].value_counts()
            st.markdown("### 💳 Payment Method Breakdown")
            
            payment_cols = st.columns(len(payment_breakdown))
            
            for idx, (method, count) in enumerate(payment_breakdown.items()):
                revenue = orders_df[orders_df['payment_method'] == method]['grand_total'].sum()
                
                with payment_cols[idx]:
                    st.markdown(f"""
                    <div class="summary-card">
                        <h4>{method}</h4>
                        <p>Orders: {count}</p>
                        <p>Revenue: ₹{revenue:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Bills list
            st.markdown("### 📄 Bills List")
            
            # Search functionality
            search_term = st.text_input("🔍 Search orders", placeholder="Search by order number, customer name...")
            
            if search_term:
                mask = (
                    orders_df['order_number'].str.contains(search_term, case=False, na=False) |
                    orders_df['customer_name'].str.contains(search_term, case=False, na=False)
                )
                filtered_orders = orders_df[mask]
            else:
                filtered_orders = orders_df
            
            # Pagination
            items_per_page = 10
            total_pages = len(filtered_orders) // items_per_page + (1 if len(filtered_orders) % items_per_page > 0 else 0)
            
            if total_pages > 0:
                page = st.selectbox("Page", range(1, total_pages + 1))
                start_idx = (page - 1) * items_per_page
                end_idx = start_idx + items_per_page
                page_orders = filtered_orders.iloc[start_idx:end_idx]
            else:
                page_orders = filtered_orders
            
            # Display orders
            for _, order in page_orders.iterrows():
                items_data = json.loads(str(order['items_json'])) if order['items_json'] else []
                
                st.markdown(f"""
                <div class="bill-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4>🧾 {order['order_number']}</h4>
                            <p><strong>Date:</strong> {order['order_date']}</p>
                            <p><strong>Service:</strong> {order['service_mode']}</p>
                            <p><strong>Customer:</strong> {str(order['customer_name']) if order['customer_name'] else 'Walk-in'}</p>
                            {f"<p><strong>Phone:</strong> {str(order['customer_phone'])}</p>" if order['customer_phone'] else ""}
                            {f"<p><strong>Table:</strong> {str(order['table_number'])}</p>" if order['table_number'] else ""}
                        </div>
                        <div style="text-align: right;">
                            <h3>₹{order['grand_total']:.2f}</h3>
                            <p>{order['payment_method']}</p>
                            <p>Items: {len(items_data)}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    if st.button("👁️ View Details", key=f"view_{order['id']}"):
                        st.session_state.selected_order = order['id']
                
                with col2:
                    if st.button("📄 View Bill", key=f"bill_{order['id']}"):
                        # Generate and show bill
                        order_data = {
                            'order_number': order['order_number'],
                            'service_mode': order['service_mode'],
                            'customer_name': order['customer_name'],
                            'customer_phone': order['customer_phone'],
                            'table_number': order['table_number'],
                            'payment_method': order['payment_method'],
                            'order_date': order['order_date'],
                            'order_status': order['order_status']
                        }
                        
                        calculations = {
                            'subtotal': order['subtotal'],
                            'gst_amount': order['gst_amount'],
                            'discount_amount': order['discount_amount'],
                            'grand_total': order['grand_total']
                        }
                        
                        bill_text = generate_bill_text(order_data, items_data, calculations)
                        
                        st.markdown(f"### 🧾 Bill - {order['order_number']}")
                        st.code(bill_text, language="text")
                        
                        st.download_button(
                            label="📥 Download Bill",
                            data=bill_text,
                            file_name=f"bill_{order['order_number']}.txt",
                            mime="text/plain",
                            key=f"download_{order['id']}"
                        )
                
                with col3:
                    # Export order as JSON
                    order_json = {
                        'order_data': order.to_dict(),
                        'items': items_data
                    }
                    
                    st.download_button(
                        label="📥 JSON",
                        data=json.dumps(order_json, indent=2, default=str),
                        file_name=f"order_{order['order_number']}.json",
                        mime="application/json",
                        key=f"json_{order['id']}"
                    )
                
                with col4:
                    if order['customer_phone'] and st.button("📱 WhatsApp", key=f"whatsapp_{order['id']}"):
                        # Generate WhatsApp message (for future implementation)
                        st.info("WhatsApp integration coming soon!")
            
            # Export all filtered orders
            st.markdown("### 📥 Export Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = filtered_orders.to_csv(index=False)
                st.download_button(
                    label="📥 Download Orders as CSV",
                    data=csv_data,
                    file_name=f"orders_{from_date}_to_{to_date}.csv",
                    mime="text/csv"
                )
            
            with col2:
                json_data = filtered_orders.to_json(orient='records', indent=2, default=str)
                st.download_button(
                    label="📥 Download Orders as JSON",
                    data=json_data,
                    file_name=f"orders_{from_date}_to_{to_date}.json",
                    mime="application/json"
                )
        
        except Exception as e:
            st.error(f"Error loading bills: {str(e)}")
    
    # Order details modal
    if 'selected_order' in st.session_state:
        try:
            orders_df = get_orders()
            selected_order = orders_df[orders_df['id'] == st.session_state.selected_order].iloc[0]
            items_data = json.loads(selected_order['items_json']) if selected_order['items_json'] else []
            
            st.markdown("### 📋 Order Details")
            
            # Order information
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                **Order Number:** {selected_order['order_number']}  
                **Date & Time:** {selected_order['order_date']}  
                **Service Mode:** {selected_order['service_mode']}  
                **Payment Method:** {selected_order['payment_method']}  
                """)
            
            with col2:
                st.markdown(f"""
                **Customer:** {selected_order['customer_name'] if selected_order['customer_name'] else 'Walk-in'}  
                **Phone:** {selected_order['customer_phone'] if selected_order['customer_phone'] else 'N/A'}  
                **Table:** {selected_order['table_number'] if selected_order['table_number'] else 'N/A'}  
                **Status:** {selected_order['order_status']}  
                """)
            
            # Order items
            st.markdown("#### 🍽️ Items Ordered")
            
            items_df = pd.DataFrame(items_data)
            if not items_df.empty:
                items_df['total'] = items_df['price'] * items_df['quantity']
                st.dataframe(
                    items_df[['name', 'category', 'quantity', 'price', 'total']],
                    use_container_width=True
                )
            
            # Order totals
            st.markdown("#### 💰 Order Summary")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Subtotal", f"₹{selected_order['subtotal']:.2f}")
            
            with col2:
                st.metric("GST", f"₹{selected_order['gst_amount']:.2f}")
            
            with col3:
                st.metric("Discount", f"₹{selected_order['discount_amount']:.2f}")
            
            with col4:
                st.metric("Grand Total", f"₹{selected_order['grand_total']:.2f}")
            
            if st.button("❌ Close Details"):
                st.session_state.pop('selected_order', None)
                st.rerun()
        
        except Exception as e:
            st.error(f"Error loading order details: {str(e)}")
            st.session_state.pop('selected_order', None)

if __name__ == "__main__":
    main()
