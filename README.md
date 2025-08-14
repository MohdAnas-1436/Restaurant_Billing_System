# Royal Restaurant Billing System

A comprehensive offline restaurant billing system built with Streamlit featuring warm royal colors, SQLite database, and complete order management capabilities.

## Features

### 🍽️ Core Functionality
- **Dual Service Modes**: Dine-In and Takeaway service options
- **Complete Menu Management**: Add, edit, delete, and categorize menu items
- **Interactive Order Entry**: Real-time order building with quantity management
- **Professional Bill Generation**: Itemized bills with GST calculations
- **Multiple Payment Methods**: Cash, Card, UPI, and Net Banking support
- **Comprehensive Reporting**: Daily, weekly, monthly sales analytics

### 🎨 Design Features
- **Warm Royal Color Scheme**: Deep purples, golds, and rich burgundy
- **Responsive Interface**: Works on desktop and tablet devices
- **Professional Layout**: Clean, intuitive design for cashier operations
- **Custom Styling**: Beautiful gradients and modern UI components

### 📊 Business Intelligence
- **Sales Dashboard**: Real-time performance metrics
- **Top Selling Items**: Most popular menu items analytics
- **Payment Analysis**: Payment method breakdown and trends
- **Service Mode Tracking**: Dine-in vs Takeaway performance
- **Hourly Sales Patterns**: Peak hours identification
- **Export Capabilities**: CSV and JSON export for all data

### 💾 Data Management
- **SQLite Database**: Complete offline functionality
- **Transaction History**: Detailed order tracking and history
- **Customer Information**: Name, phone, and table management
- **Inventory Tracking**: Menu item availability status
- **Data Export**: Bills and reports in multiple formats

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Windows/Linux/Mac OS

### Quick Start

1. **Download the Project**
   ```bash
   # Download and extract the project files
   ```

2. **Install Dependencies**
   ```bash
   pip install streamlit pandas plotly sqlite3
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py --server.port 5000
   ```

4. **Access the Application**
   - Open your browser to `http://localhost:5000`
   - The application will automatically initialize with sample data

## Application Structure

```
restaurant_billing/
├── app.py                      # Main application entry point
├── run_restaurant.py           # Offline startup script
├── setup_requirements.txt      # Python dependencies
│
├── .streamlit/
│   └── config.toml            # Streamlit configuration
│
├── pages/                     # Multi-page application
│   ├── 1_Menu_Management.py   # Menu CRUD operations
│   ├── 2_Order_Entry.py       # Order creation and billing
│   ├── 3_Bills_History.py     # Transaction history
│   └── 4_Reports.py           # Analytics and reporting
│
├── db/
│   ├── db_utils.py            # Database operations
│   └── restaurant.db          # SQLite database (auto-created)
│
├── utils/
│   └── calculator.py          # Order calculations and bill generation
│
├── data/
│   └── sample_menu.csv        # Sample menu data
│
└── README.md                  # This file
```

## Offline Setup Instructions

### For Windows PC

1. **Download the Project**
   - Download all project files to a folder (e.g., `C:\restaurant_billing\`)
   - Ensure all files and folders maintain the structure shown above

2. **Install Python**
   - Download Python 3.7+ from https://python.org
   - During installation, check "Add Python to PATH"
   - Verify installation: Open Command Prompt and type `python --version`

3. **Easy Startup (Recommended)**
   ```cmd
   cd C:\restaurant_billing
   python run_restaurant.py
   ```
   This script will automatically:
   - Check Python version
   - Install required packages
   - Create necessary directories
   - Initialize the database
   - Start the application

4. **Manual Setup (Alternative)**
   ```cmd
   cd C:\restaurant_billing
   pip install streamlit pandas plotly
   streamlit run app.py --server.port 5000
   ```

5. **Access the Application**
   - Open your web browser
   - Go to: `http://localhost:5000`
   - The application will load with sample menu data

### For Mac/Linux

1. **Download and Setup**
   ```bash
   cd ~/restaurant_billing
   python3 run_restaurant.py
   ```

2. **Manual Setup (Alternative)**
   ```bash
   pip3 install streamlit pandas plotly
   streamlit run app.py --server.port 5000
   ```

## Features Overview

### 🎨 Royal Theme Design
- Deep purple and gold color scheme
- Gradient backgrounds and modern UI
- Professional restaurant interface
- Responsive design for desktop/tablet

### 📋 Menu Management
- Add, edit, delete menu items
- Categorize items (Appetizers, Main Course, etc.)
- Set prices and GST rates
- Control item availability
- Export menu as CSV/JSON

### 🛒 Order Entry
- Select Dine-In or Takeaway mode
- Browse menu by category
- Search items by name
- Add items to cart with quantities
- Apply discounts
- Multiple payment methods
- Generate professional bills

### 📄 Bills History
- View all transaction history
- Filter by date ranges
- Search orders by customer/order number
- Export bills in text format
- Download order data as JSON/CSV

### 📊 Reports & Analytics
- Daily sales trends
- Top-selling items analysis
- Payment method breakdowns
- Service mode performance
- Hourly sales patterns
- Export all reports

## Database Schema

### Tables
- **menu**: Item catalog with pricing and categories
- **orders**: Complete transaction records
- **order_items**: Detailed line items for each order

### Sample Data
The application includes 24 sample menu items across 5 categories to demonstrate functionality.

## Troubleshooting

### Application Won't Start
1. Ensure Python 3.7+ is installed
2. Check all required files are present
3. Run: `python run_restaurant.py` for automatic setup
4. Verify no other application is using port 5000

### "Webpage Not Found" Error
1. Wait 10-15 seconds after starting for application to load
2. Try: `http://localhost:5000` instead of `http://127.0.0.1:5000`
3. Check firewall isn't blocking the connection
4. Restart the application

### Database Issues
1. Delete `db/restaurant.db` file and restart
2. Application will recreate database with sample data
3. Ensure write permissions in the application folder

### Package Installation Issues
```cmd
python -m pip install --upgrade pip
pip install streamlit pandas plotly
```

## Advanced Configuration

### Customizing Colors
Edit `.streamlit/config.toml` to change theme colors:
```toml
[theme]
primaryColor = "#D4AF37"           # Gold
backgroundColor = "#1A0B2E"        # Dark purple
secondaryBackgroundColor = "#2D1B3D"
textColor = "#F5F5DC"              # Cream
```

### Port Configuration
Change port in startup command:
```cmd
streamlit run app.py --server.port 8501
```

## Support

This is a complete offline restaurant billing system. All data is stored locally in SQLite database. No internet connection required after initial setup.

For best experience:
- Use Chrome, Firefox, or Edge browser
- Keep terminal/command prompt window open while using
- Regularly backup the `db/restaurant.db` file
- Export important data using the built-in export features

