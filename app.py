import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import json
import os
from db.db_utils import init_database, get_menu_items, add_sample_menu
from utils.calculator import calculate_order_total

# Page configuration
st.set_page_config(
    page_title="Royal Restaurant Billing System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for warm royal colors
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #4A148C, #7B1FA2, #AD1457);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        color: #FFD700;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .service-card {
        background: linear-gradient(135deg, #6A1B9A, #8E24AA);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease;
    }
    
    .service-card:hover {
        transform: translateY(-5px);
    }
    
    .order-summary {
        background: linear-gradient(135deg, #4A148C, #6A1B9A);
        padding: 1.5rem;
        border-radius: 10px;
        color: #FFD700;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #7B1FA2, #AD1457);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #D4AF37, #FFD700);
        color: #4A148C;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #FFD700, #FFA000);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2D1B3D, #4A148C);
    }
</style>
""", unsafe_allow_html=True)

def initialize_app():
    """Initialize the application and database"""
    if not os.path.exists('db'):
        os.makedirs('db')
    
    init_database()
    
    # Add sample menu if menu is empty
    menu_items = get_menu_items()
    if menu_items.empty:
        add_sample_menu()

def main():
    # Initialize the app
    initialize_app()
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🍽️ Royal Restaurant Billing System</h1>
        <p>Premium Dining Experience with Professional Billing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_order' not in st.session_state:
        st.session_state.current_order = []
    if 'service_mode' not in st.session_state:
        st.session_state.service_mode = None
    if 'customer_info' not in st.session_state:
        st.session_state.customer_info = {}
    
    # Main dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="service-card">
            <h3>🏠 Dine-In Service</h3>
            <p>Full restaurant experience with table service</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Dine-In Order", key="dine_in", use_container_width=True):
            st.session_state.service_mode = "Dine-In"
            st.session_state.current_order = []
            st.success("Dine-In mode selected! Go to Order Entry to continue.")
    
    with col2:
        st.markdown("""
        <div class="service-card">
            <h3>🥡 Takeaway Service</h3>
            <p>Quick pickup orders for customers on the go</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Takeaway Order", key="takeaway", use_container_width=True):
            st.session_state.service_mode = "Takeaway"
            st.session_state.current_order = []
            st.success("Takeaway mode selected! Go to Order Entry to continue.")
    
    with col3:
        st.markdown("""
        <div class="service-card">
            <h3>📊 Quick Stats</h3>
            <p>Today's performance overview</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Current order status
    if st.session_state.service_mode:
        st.markdown(f"""
        <div class="order-summary">
            <h3>Current Session</h3>
            <p><strong>Service Mode:</strong> {st.session_state.service_mode}</p>
            <p><strong>Items in Cart:</strong> {len(st.session_state.current_order)}</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.current_order:
            total_amount = sum(item['price'] * item['quantity'] for item in st.session_state.current_order)
            gst_amount = total_amount * 0.05
            grand_total = total_amount + gst_amount
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Subtotal</h4>
                    <h2>₹{total_amount:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>GST (5%)</h4>
                    <h2>₹{gst_amount:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Grand Total</h4>
                    <h2>₹{grand_total:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Manage Menu", use_container_width=True):
            st.switch_page("pages/1_Menu_Management.py")
    
    with col2:
        if st.button("🛒 Order Entry", use_container_width=True):
            st.switch_page("pages/2_Order_Entry.py")
    
    with col3:
        if st.button("📄 Bills History", use_container_width=True):
            st.switch_page("pages/3_Bills_History.py")
    
    with col4:
        if st.button("📊 Reports", use_container_width=True):
            st.switch_page("pages/4_Reports.py")
    
    # Today's summary
    st.markdown("### Today's Summary")
    
    try:
        conn = sqlite3.connect('db/restaurant.db')
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Get today's orders
        today_orders = pd.read_sql_query(
            "SELECT * FROM orders WHERE DATE(order_date) = ?",
            conn, params=[today]
        )
        
        if not today_orders.empty:
            total_sales = today_orders['grand_total'].sum()
            total_orders = len(today_orders)
            avg_order_value = total_sales / total_orders if total_orders > 0 else 0
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Total Sales</h4>
                    <h2>₹{total_sales:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Total Orders</h4>
                    <h2>{total_orders}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Avg Order Value</h4>
                    <h2>₹{avg_order_value:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No orders recorded for today yet.")
        
        conn.close()
        
    except Exception as e:
        st.error(f"Error loading today's summary: {str(e)}")

if __name__ == "__main__":
    main()
