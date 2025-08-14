import streamlit as st
import pandas as pd
from db.db_utils import get_menu_items, add_menu_item, update_menu_item, delete_menu_item

st.set_page_config(page_title="Menu Management", page_icon="📋", layout="wide")

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
    
    .menu-card {
        background: linear-gradient(135deg, #6A1B9A, #8E24AA);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        color: white;
    }
    
    .category-header {
        background: linear-gradient(90deg, #D4AF37, #FFD700);
        color: #4A148C;
        padding: 1rem;
        border-radius: 8px;
        font-weight: bold;
        margin: 1rem 0 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="main-header">
        <h1>📋 Menu Management</h1>
        <p>Add, edit, and manage your restaurant menu items</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for adding new items
    with st.sidebar:
        st.markdown("### Add New Menu Item")
        
        with st.form("add_item_form"):
            name = st.text_input("Item Name")
            category = st.selectbox("Category", [
                "Appetizers", "Main Course", "Bread & Rice", 
                "Beverages", "Desserts", "Chinese", "South Indian"
            ])
            price = st.number_input("Price (₹)", min_value=0.0, step=0.50)
            gst_rate = st.number_input("GST Rate (%)", min_value=0.0, max_value=28.0, value=5.0)
            
            submit_button = st.form_submit_button("Add Item")
            
            if submit_button:
                if name and price > 0:
                    try:
                        add_menu_item(name, category, price, gst_rate)
                        st.success(f"Added {name} to menu!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding item: {str(e)}")
                else:
                    st.error("Please provide valid item name and price")
    
    # Main menu display
    try:
        menu_df = get_menu_items()
        
        if menu_df.empty:
            st.warning("No menu items found. Add items using the sidebar.")
            return
        
        # Display menu by categories
        categories = menu_df['category'].unique()
        
        for category in sorted(categories):
            st.markdown(f"""
            <div class="category-header">
                <h3>{category}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            category_items = menu_df[menu_df['category'] == category]
            
            # Create columns for items
            cols = st.columns(3)
            
            for idx, (_, item) in enumerate(category_items.iterrows()):
                col_idx = idx % 3
                
                with cols[col_idx]:
                    st.markdown(f"""
                    <div class="menu-card">
                        <h4>{item['name']}</h4>
                        <p><strong>Price:</strong> ₹{item['price']:.2f}</p>
                        <p><strong>GST:</strong> {item['gst_rate']:.1f}%</p>
                        <p><strong>Status:</strong> {'Available' if bool(item['available']) else 'Unavailable'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Edit button
                    if st.button(f"✏️ Edit", key=f"edit_{item['id']}"):
                        st.session_state.edit_item_id = item['id']
                    
                    # Delete button
                    if st.button(f"🗑️ Delete", key=f"delete_{item['id']}"):
                        if st.session_state.get('confirm_delete') == item['id']:
                            try:
                                delete_menu_item(item['id'])
                                st.success(f"Deleted {item['name']}")
                                st.session_state.pop('confirm_delete', None)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error deleting item: {str(e)}")
                        else:
                            st.session_state.confirm_delete = item['id']
                            st.warning("Click delete again to confirm")
        
        # Edit item modal
        if 'edit_item_id' in st.session_state:
            item_to_edit = menu_df[menu_df['id'] == st.session_state.edit_item_id].iloc[0]
            
            st.markdown("### Edit Menu Item")
            
            with st.form("edit_item_form"):
                edit_name = st.text_input("Item Name", value=item_to_edit['name'])
                edit_category = st.selectbox("Category", [
                    "Appetizers", "Main Course", "Bread & Rice", 
                    "Beverages", "Desserts", "Chinese", "South Indian"
                ], index=["Appetizers", "Main Course", "Bread & Rice", 
                         "Beverages", "Desserts", "Chinese", "South Indian"].index(item_to_edit['category']) 
                         if item_to_edit['category'] in ["Appetizers", "Main Course", "Bread & Rice", 
                                                        "Beverages", "Desserts", "Chinese", "South Indian"] else 0)
                edit_price = st.number_input("Price (₹)", min_value=0.0, step=0.50, value=float(item_to_edit['price']))
                edit_gst_rate = st.number_input("GST Rate (%)", min_value=0.0, max_value=28.0, value=float(item_to_edit['gst_rate']))
                edit_available = st.checkbox("Available", value=bool(item_to_edit['available']))
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.form_submit_button("Update Item"):
                        try:
                            update_menu_item(
                                st.session_state.edit_item_id,
                                edit_name, edit_category, edit_price, 
                                edit_gst_rate, edit_available
                            )
                            st.success(f"Updated {edit_name}")
                            st.session_state.pop('edit_item_id', None)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error updating item: {str(e)}")
                
                with col2:
                    if st.form_submit_button("Cancel"):
                        st.session_state.pop('edit_item_id', None)
                        st.rerun()
        
        # Menu summary
        st.markdown("### Menu Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Items", len(menu_df))
        
        with col2:
            st.metric("Categories", len(categories))
        
        with col3:
            available_items = len(menu_df[menu_df['available'] == 1])
            st.metric("Available Items", available_items)
        
        with col4:
            avg_price = menu_df['price'].mean()
            st.metric("Average Price", f"₹{avg_price:.2f}")
        
        # Export menu
        st.markdown("### Export Menu")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Download as CSV"):
                csv = menu_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="menu.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📥 Download as JSON"):
                json_data = menu_df.to_json(orient='records', indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name="menu.json",
                    mime="application/json"
                )
    
    except Exception as e:
        st.error(f"Error loading menu: {str(e)}")

if __name__ == "__main__":
    main()
