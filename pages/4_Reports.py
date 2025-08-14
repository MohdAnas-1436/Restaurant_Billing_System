import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from db.db_utils import get_sales_summary, get_orders

st.set_page_config(page_title="Reports", page_icon="📊", layout="wide")

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
    
    .metric-card {
        background: linear-gradient(135deg, #6A1B9A, #8E24AA);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 1rem 0;
    }
    
    .chart-container {
        background: linear-gradient(135deg, #4A148C, #6A1B9A);
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="main-header">
        <h1>📊 Sales Reports & Analytics</h1>
        <p>Comprehensive business insights and performance metrics</p>
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
        if st.button("📊 Generate Reports", type="primary"):
            st.session_state.generate_reports = True
    
    # Quick date filters
    st.markdown("**Quick Filters:**")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    quick_filters = [
        ("Today", timedelta(days=0)),
        ("Yesterday", timedelta(days=1)),
        ("Last 7 Days", timedelta(days=7)),
        ("Last 30 Days", timedelta(days=30)),
        ("Last 3 Months", timedelta(days=90))
    ]
    
    for idx, (label, delta) in enumerate(quick_filters):
        with [col1, col2, col3, col4, col5][idx]:
            if st.button(f"📅 {label}"):
                if label == "Yesterday":
                    yesterday = datetime.now().date() - timedelta(days=1)
                    st.session_state.date_from = yesterday
                    st.session_state.date_to = yesterday
                elif label == "Today":
                    st.session_state.date_from = datetime.now().date()
                    st.session_state.date_to = datetime.now().date()
                else:
                    st.session_state.date_from = datetime.now().date() - delta
                    st.session_state.date_to = datetime.now().date()
                st.session_state.generate_reports = True
    
    # Generate reports
    if st.session_state.get('generate_reports'):
        try:
            # Get date range
            from_date = st.session_state.get('date_from', date_from)
            to_date = st.session_state.get('date_to', date_to)
            
            # Get sales data
            daily_sales, most_sold, payment_breakdown = get_sales_summary(
                from_date.strftime('%Y-%m-%d'),
                to_date.strftime('%Y-%m-%d')
            )
            
            if daily_sales.empty:
                st.warning("No sales data found for the selected date range.")
                return
            
            # Key metrics
            st.markdown("### 📈 Key Performance Metrics")
            
            total_sales = daily_sales['total_sales'].sum()
            total_orders = daily_sales['total_orders'].sum()
            avg_order_value = total_sales / total_orders if total_orders > 0 else 0
            best_day_sales = daily_sales['total_sales'].max() if not daily_sales.empty else 0
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Total Revenue</h4>
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
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Best Day Sales</h4>
                    <h2>₹{best_day_sales:.2f}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # Daily sales trend
            st.markdown("### 📈 Daily Sales Trend")
            
            if len(daily_sales) > 1:
                fig_sales = px.line(
                    daily_sales, 
                    x='date', 
                    y='total_sales',
                    title='Daily Sales Revenue',
                    color_discrete_sequence=['#FFD700']
                )
                fig_sales.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_sales, use_container_width=True)
                
                # Orders trend
                fig_orders = px.bar(
                    daily_sales, 
                    x='date', 
                    y='total_orders',
                    title='Daily Order Count',
                    color_discrete_sequence=['#D4AF37']
                )
                fig_orders.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_orders, use_container_width=True)
            
            else:
                st.info("Need more data points to show trends. Select a longer date range.")
            
            # Top selling items
            st.markdown("### 🏆 Top Selling Items")
            
            if not most_sold.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Top items by quantity
                    fig_qty = px.bar(
                        most_sold.head(10), 
                        x='total_quantity', 
                        y='item_name',
                        title='Top Items by Quantity Sold',
                        orientation='h',
                        color_discrete_sequence=['#8E24AA']
                    )
                    fig_qty.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig_qty, use_container_width=True)
                
                with col2:
                    # Top items by revenue
                    fig_rev = px.bar(
                        most_sold.head(10), 
                        x='total_revenue', 
                        y='item_name',
                        title='Top Items by Revenue',
                        orientation='h',
                        color_discrete_sequence=['#AD1457']
                    )
                    fig_rev.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig_rev, use_container_width=True)
                
                # Most sold items table
                st.markdown("#### 📋 Detailed Top Items")
                st.dataframe(
                    most_sold.head(20),
                    use_container_width=True
                )
            
            # Payment method analysis
            st.markdown("### 💳 Payment Method Analysis")
            
            if not payment_breakdown.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Payment method pie chart
                    fig_payment = px.pie(
                        payment_breakdown,
                        values='total_amount',
                        names='payment_method',
                        title='Revenue by Payment Method'
                    )
                    fig_payment.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig_payment, use_container_width=True)
                
                with col2:
                    # Payment method order count
                    fig_payment_orders = px.bar(
                        payment_breakdown,
                        x='payment_method',
                        y='order_count',
                        title='Orders by Payment Method',
                        color_discrete_sequence=['#7B1FA2']
                    )
                    fig_payment_orders.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig_payment_orders, use_container_width=True)
            
            # Service mode analysis
            st.markdown("### 🍽️ Service Mode Analysis")
            
            orders_df = get_orders(
                from_date.strftime('%Y-%m-%d'),
                to_date.strftime('%Y-%m-%d')
            )
            
            if not orders_df.empty:
                service_summary = orders_df.groupby('service_mode').agg({
                    'id': 'count',
                    'grand_total': ['sum', 'mean']
                }).round(2)
                
                service_summary.columns = ['Order Count', 'Total Revenue', 'Avg Order Value']
                service_summary = service_summary.reset_index()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Service mode revenue
                    fig_service = px.pie(
                        service_summary,
                        values='Total Revenue',
                        names='service_mode',
                        title='Revenue by Service Mode'
                    )
                    fig_service.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig_service, use_container_width=True)
                
                with col2:
                    st.markdown("#### 📊 Service Mode Summary")
                    st.dataframe(service_summary, use_container_width=True)
            
            # Hourly analysis (if same day data)
            if from_date == to_date:
                st.markdown("### 🕐 Hourly Sales Pattern")
                
                orders_df['hour'] = pd.to_datetime(orders_df['order_date']).dt.hour
                hourly_sales = orders_df.groupby('hour').agg({
                    'id': 'count',
                    'grand_total': 'sum'
                }).reset_index()
                hourly_sales.columns = ['hour', 'order_count', 'total_sales']
                
                if not hourly_sales.empty:
                    fig_hourly = px.bar(
                        hourly_sales,
                        x='hour',
                        y='total_sales',
                        title='Hourly Sales Distribution',
                        color_discrete_sequence=['#6A1B9A']
                    )
                    fig_hourly.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font_color='white'
                    )
                    st.plotly_chart(fig_hourly, use_container_width=True)
            
            # Export reports
            st.markdown("### 📥 Export Reports")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if not daily_sales.empty:
                    csv_daily = daily_sales.to_csv(index=False)
                    st.download_button(
                        label="📥 Daily Sales CSV",
                        data=csv_daily,
                        file_name=f"daily_sales_{from_date}_to_{to_date}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if not most_sold.empty:
                    csv_items = most_sold.to_csv(index=False)
                    st.download_button(
                        label="📥 Top Items CSV",
                        data=csv_items,
                        file_name=f"top_items_{from_date}_to_{to_date}.csv",
                        mime="text/csv"
                    )
            
            with col3:
                if not payment_breakdown.empty:
                    csv_payment = payment_breakdown.to_csv(index=False)
                    st.download_button(
                        label="📥 Payment Analysis CSV",
                        data=csv_payment,
                        file_name=f"payment_analysis_{from_date}_to_{to_date}.csv",
                        mime="text/csv"
                    )
            
            # Business insights
            st.markdown("### 💡 Business Insights")
            
            insights = []
            
            # Best performing day
            if not daily_sales.empty and len(daily_sales) > 1:
                best_day = daily_sales.loc[daily_sales['total_sales'].idxmax()]
                insights.append(f"🏆 Best performing day: {best_day['date']} with ₹{best_day['total_sales']:.2f} sales")
            
            # Top selling item
            if not most_sold.empty:
                top_item = most_sold.iloc[0]
                insights.append(f"🥇 Top selling item: {top_item['item_name']} ({top_item['total_quantity']} units sold)")
            
            # Most used payment method
            if not payment_breakdown.empty:
                top_payment = payment_breakdown.loc[payment_breakdown['total_amount'].idxmax()]
                insights.append(f"💳 Most popular payment method: {top_payment['payment_method']} (₹{top_payment['total_amount']:.2f})")
            
            # Average order insights
            if avg_order_value > 0:
                if avg_order_value > 500:
                    insights.append("📈 High average order value indicates premium customer base")
                elif avg_order_value < 200:
                    insights.append("💡 Consider upselling strategies to increase average order value")
            
            for insight in insights:
                st.info(insight)
        
        except Exception as e:
            st.error(f"Error generating reports: {str(e)}")

if __name__ == "__main__":
    main()
