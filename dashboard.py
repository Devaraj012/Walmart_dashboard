pip install plotly
pip install openpyxl
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Title of the app
st.title("Walmart Data Dashboard")

# Upload Walmart Data
uploaded_file = st.file_uploader("Upload Walmart Data File (CSV or Excel)", type=["csv", "xlsx"])

# Load and display data
if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1]
    
    if file_extension == 'csv':
        data = pd.read_csv(uploaded_file)
    elif file_extension == 'xlsx':
        data = pd.read_excel(uploaded_file)

    # Convert dates
    data['Order Date'] = pd.to_datetime(data['Order Date'], errors='coerce')
    data['Ship Date'] = pd.to_datetime(data['Ship Date'], errors='coerce')

    # Buttons for page navigation
    col1, col2, col3 = st.columns(3)
    with col1:
        overview_button = st.button("Overview")
    with col2:
        product_button = st.button("Products")
    with col3:
        customer_button = st.button("Customers")

    # Page Content
    if overview_button:
        st.subheader("Overview of the Data")
        
        # Displaying content in a card format
        with st.container():
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.write("**Dataset Summary:**")
            total_records = len(data)
            unique_countries = data['Country'].nunique()
            unique_segments = data['Segment'].nunique()
            unique_categories = data['Category'].nunique()
            
            st.write(f"Total Records: {total_records}")
            st.write(f"Unique Countries: {unique_countries}")
            st.write(f"Unique Segments: {unique_segments}")
            st.write(f"Unique Product Categories: {unique_categories}")
            st.markdown('</div>', unsafe_allow_html=True)

            # Descriptive statistics for numerical columns
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.write("**Descriptive Statistics (Sales, Profit, etc.):**")
            st.write(data[['Sales', 'Profit', 'Quantity']].describe())
            st.markdown('</div>', unsafe_allow_html=True)

            # Additional insights (e.g., missing values)
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            missing_values = data.isnull().sum()
            st.write(f"**Missing Values per Column:**")
            st.write(missing_values[missing_values > 0])
            st.markdown('</div>', unsafe_allow_html=True)

    elif product_button:
        st.subheader("Product Insights")

        # Top 10 Products by Sales
        top_10_products_sales = data.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
        st.write("Top 10 Products by Sales:")

        # Plotly chart for Sales by Product
        fig_sales = px.bar(top_10_products_sales, x=top_10_products_sales.index, y=top_10_products_sales.values,
                           labels={'x': 'Product Name', 'y': 'Total Sales'},
                           title="Top 10 Products by Sales")
        st.plotly_chart(fig_sales)

        # Top 10 Products by Profit
        top_10_products_profit = data.groupby('Product Name')['Profit'].sum().sort_values(ascending=False).head(10)
        st.write("Top 10 Products by Profit:")

        # Plotly chart for Profit by Product
        fig_profit = px.bar(top_10_products_profit, x=top_10_products_profit.index, y=top_10_products_profit.values,
                            labels={'x': 'Product Name', 'y': 'Total Profit'},
                            title="Top 10 Products by Profit")
        st.plotly_chart(fig_profit)

        # Top 10 Products by Quantity
        top_10_products_quantity = data.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(10)
        st.write("Top 10 Products by Quantity:")

        # Plotly chart for Quantity by Product
        fig_quantity = px.bar(top_10_products_quantity, x=top_10_products_quantity.index, y=top_10_products_quantity.values,
                              labels={'x': 'Product Name', 'y': 'Quantity Sold'},
                              title="Top 10 Products by Quantity Sold")
        st.plotly_chart(fig_quantity)

        # Top 10 Products by Discount
        top_10_products_discount = data.groupby('Product Name')['Discount'].mean().sort_values(ascending=False).head(10)
        st.write("Top 10 Products by Average Discount:")

        # Plotly chart for Discount by Product
        fig_discount = px.bar(top_10_products_discount, x=top_10_products_discount.index, y=top_10_products_discount.values,
                              labels={'x': 'Product Name', 'y': 'Average Discount'},
                              title="Top 10 Products by Average Discount")
        st.plotly_chart(fig_discount)

        # Sales by Product Category (Altair chart)
        category_sales = data.groupby('Category')['Sales'].sum().sort_values(ascending=False)
        st.write("Top 10 Sales by Product Category:")

        category_chart = alt.Chart(category_sales.head(10).reset_index()).mark_bar().encode(
            x='Category',
            y='Sales',
            color='Category',
            tooltip=['Category', 'Sales']
        ).properties(title="Top 10 Sales by Category")
        st.altair_chart(category_chart, use_container_width=True)

        # Sales Quantity by Sub-Category (Plotly chart)
        sub_category_sales = data.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False)
        st.write("Top 10 Sales by Sub-Category:")

        fig_sub_category = px.bar(sub_category_sales.head(10), x=sub_category_sales.head(10).index, y=sub_category_sales.head(10).values,
                                  labels={'x': 'Sub-Category', 'y': 'Total Sales'},
                                  title="Top 10 Sales by Sub-Category")
        st.plotly_chart(fig_sub_category)

    elif customer_button:
        st.subheader("Customer Insights")

        # Top 10 Customers by Sales
        top_10_customers_sales = data.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10)
        st.write("Top 10 Customers by Sales:")

        # Plotly chart for Sales by Customer
        fig_sales_customers = px.bar(top_10_customers_sales, x=top_10_customers_sales.index, y=top_10_customers_sales.values,
                                     labels={'x': 'Customer Name', 'y': 'Total Sales'},
                                     title="Top 10 Customers by Sales")
        st.plotly_chart(fig_sales_customers)

        # Top 10 Customers by Quantity Purchased
        top_10_customers_quantity = data.groupby('Customer Name')['Quantity'].sum().sort_values(ascending=False).head(10)
        st.write("Top 10 Customers by Quantity Purchased:")

        # Plotly chart for Quantity Purchased by Customer
        fig_quantity_customers = px.bar(top_10_customers_quantity, x=top_10_customers_quantity.index, y=top_10_customers_quantity.values,
                                       labels={'x': 'Customer Name', 'y': 'Total Quantity Purchased'},
                                       title="Top 10 Customers by Quantity Purchased")
        st.plotly_chart(fig_quantity_customers)

        # Top 10 Customers by Profit
        top_10_customers_profit = data.groupby('Customer Name')['Profit'].sum().sort_values(ascending=False).head(10)
        st.write("Top 10 Customers by Profit:")

        # Plotly chart for Profit by Customer
        fig_profit_customers = px.bar(top_10_customers_profit, x=top_10_customers_profit.index, y=top_10_customers_profit.values,
                                      labels={'x': 'Customer Name', 'y': 'Total Profit'},
                                      title="Top 10 Customers by Profit")
        st.plotly_chart(fig_profit_customers)

        # Top 10 Customers by Discount Given
        top_10_customers_discount = data.groupby('Customer Name')['Discount'].mean().sort_values(ascending=False).head(10)
        st.write("Top 10 Customers by Average Discount:")

        # Plotly chart for Discount by Customer
        fig_discount_customers = px.bar(top_10_customers_discount, x=top_10_customers_discount.index, y=top_10_customers_discount.values,
                                        labels={'x': 'Customer Name', 'y': 'Average Discount'},
                                        title="Top 10 Customers by Average Discount")
        st.plotly_chart(fig_discount_customers)

        # Sales by Customer Segment (Altair chart)
        segment_sales = data.groupby('Segment')['Sales'].sum().sort_values(ascending=False)
        st.write("Top 10 Sales by Customer Segment:")

        segment_chart = alt.Chart(segment_sales.head(10).reset_index()).mark_bar().encode(
            x='Segment',
            y='Sales',
            color='Segment',
            tooltip=['Segment', 'Sales']
        ).properties(title="Top 10 Sales by Segment")
        st.altair_chart(segment_chart, use_container_width=True)

        # Top 10 Customers by Number of Orders (Plotly chart)
        top_10_customers_orders = data.groupby('Customer Name')['Order ID'].nunique().sort_values(ascending=False).head(10)
        st.write("Top 10 Customers by Number of Orders:")

        fig_orders_customers = px.bar(top_10_customers_orders, x=top_10_customers_orders.index, y=top_10_customers_orders.values,
                                      labels={'x': 'Customer Name', 'y': 'Number of Orders'},
                                      title="Top 10 Customers by Number of Orders")
        st.plotly_chart(fig_orders_customers)

else:
    st.warning("Please upload a CSV or Excel file to proceed.")
