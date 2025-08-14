# Royal Restaurant Billing System

## Overview

A comprehensive offline restaurant billing system built with Streamlit that provides complete order management, menu administration, and business analytics for restaurants. The system features a warm royal color scheme with deep purples and gold accents, supports both dine-in and takeaway services, and operates entirely offline using SQLite for data persistence. The application includes real-time order processing, professional bill generation, payment method tracking, and comprehensive reporting capabilities for restaurant operations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit-based web interface with multi-page architecture
- **UI Design**: Custom CSS with royal color scheme (deep purples, golds, burgundy) featuring gradient backgrounds and responsive layouts
- **Page Structure**: Main app with dedicated pages for Menu Management, Order Entry, Bills History, and Reports
- **State Management**: Streamlit session state for managing order cart and user interactions

### Backend Architecture
- **Database**: SQLite database with three core tables:
  - `menu`: Item catalog with pricing, categories, GST rates, and availability
  - `orders`: Complete transaction records with customer info and payment details
  - `order_items`: Detailed line items for each order
- **Data Layer**: Centralized database utilities in `db/db_utils.py` for all CRUD operations
- **Business Logic**: Order calculations, GST computation (5% standard), and discount handling in `utils/calculator.py`

### Core Features
- **Dual Service Modes**: Dine-in and takeaway order processing
- **Real-time Order Building**: Interactive cart system with quantity management
- **Payment Processing**: Support for Cash, Card, UPI, and Net Banking
- **Bill Generation**: Professional itemized bills with tax breakdowns
- **Menu Management**: Full CRUD operations for menu items with categorization
- **Analytics Dashboard**: Sales performance, top-selling items, and payment method analysis

### Data Storage Solutions
- **Primary Database**: SQLite (`restaurant.db`) for complete offline functionality
- **Data Export**: CSV and JSON export capabilities for orders and reports
- **Transaction Tracking**: Complete order history with timestamps and customer information
- **Reporting Data**: Aggregated sales data for business intelligence

## External Dependencies

### Core Python Libraries
- **Streamlit**: Web framework for the user interface and multi-page application structure
- **SQLite3**: Built-in database engine for persistent data storage
- **Pandas**: Data manipulation and analysis for reporting and export functionality
- **Plotly**: Interactive charts and visualizations for the analytics dashboard

### Additional Libraries
- **datetime**: Timestamp management for orders and reporting
- **json**: Data serialization for order items storage and export features

### Database Schema
- Menu items with pricing, categories, GST rates, and availability status
- Order tracking with customer information, service modes, and payment methods
- Detailed order items for comprehensive transaction history
- Built-in data validation and referential integrity