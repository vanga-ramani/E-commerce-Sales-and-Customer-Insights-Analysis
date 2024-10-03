# Install SQLite for SQL queries and openpyxl for Excel operations
!pip install openpyxl
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
# Create sample e-commerce data: orders, customers, products
customers = pd.DataFrame({
    'customer_id': [1, 2, 3],
    'customer_name': ['John Doe', 'Jane Smith', 'Alice Brown'],
    'customer_segment': ['Regular', 'VIP', 'Regular']
})

products = pd.DataFrame({
    'product_id': [101, 102, 103],
    'product_name': ['Laptop', 'Smartphone', 'Headphones'],
    'category': ['Electronics', 'Electronics', 'Accessories'],
    'price': [1200, 800, 100]
})

orders = pd.DataFrame({
    'order_id': [1001, 1002, 1003],
    'customer_id': [1, 2, 3],
    'product_id': [101, 102, 103],
    'quantity': [2, 1, 4],
    'order_date': ['2023-01-15', '2023-02-20', '2023-03-05']
})
# Create SQLite database in memory
conn = sqlite3.connect(':memory:')

# Load data into SQLite tables
customers.to_sql('customers', conn, index=False, if_exists='replace')
products.to_sql('products', conn, index=False, if_exists='replace')
orders.to_sql('orders', conn, index=False, if_exists='replace')
# SQL query to get total sales per product
query = """
SELECT p.product_name, SUM(o.quantity * p.price) as total_sales
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_sales DESC;
"""
total_sales = pd.read_sql_query(query, conn)
print(total_sales)
# Get customer purchase summary (total quantity per customer)
customer_summary = orders.groupby('customer_id').agg({
    'quantity': 'sum'
}).reset_index()

# Join with customer details
customer_summary = customer_summary.merge(customers, on='customer_id', how='left')
print(customer_summary)
# Add a 'high_value_customer' flag based on customer segment
customer_summary['high_value_customer'] = customer_summary['customer_segment'].apply(
    lambda x: 'Yes' if x == 'VIP' else 'No'
)
print(customer_summary)
# Bar plot of total sales per product
plt.bar(total_sales['product_name'], total_sales['total_sales'], color='skyblue')
plt.title('Total Sales by Product')
plt.xlabel('Product Name')
plt.ylabel('Total Sales')
plt.show()
# Pivot table for quantity of products sold by customer segment
pivot_table = pd.pivot_table(orders.merge(customers, on='customer_id'),
                             values='quantity', 
                             index='customer_segment', 
                             columns='product_id', 
                             aggfunc='sum', fill_value=0)
print(pivot_table)
# Save customer summary to Excel
customer_summary.to_excel('customer_summary.xlsx', index=False)
print('Excel file saved: customer_summary.xlsx')
from google.colab import files

# Download the Excel file
files.download('customer_summary.xlsx')
