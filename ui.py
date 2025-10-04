import base64 #background image
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie  
import requests  
import streamlit as st
import pandas as pd
import plotly.express as px 
from db import create_connection, reg, view
import os

#Page Configuration
st.set_page_config(
    page_title="Ecommerce Analysis", 
    page_icon="🛒", 
    layout="wide"
    )

# Initialize session state
if 'section' not in st.session_state:
    st.session_state.section = 'home'

# Sidebar navigation
def encode_image_to_base64(image_path):
    """Reads an image file and encodes it as a Base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

#image_path = r"C:\Users\HP\data science O7\1_aPROJECT\bg.jpg"
image_path = "bg.jpg"
base64_string = encode_image_to_base64(image_path)
#print(base64_string)
#st.write(base64_string)

background_style = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{base64_string}");
    background-size: cover;
}}
</style>
"""
st.markdown(background_style, unsafe_allow_html=True)

# === Light Overlay to Soften Contrast with st.markdown with css
overlay_style = """
<style>
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-color: rgba(255, 255, 255, 0.95); /* adjust opacity here */
    z-index: 0;
}
</style>
"""
st.markdown(overlay_style, unsafe_allow_html=True)
#st.title("Ecommerce Analysis")

#for gif use website Lottiefiles
#Load Function
def load_lottie_url(url):
    r=requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#st.title("Lottie Animation in Streamlit")
# # Replace with your Lottie animation URL
lottie_url = "https://lottie.host/a668460c-a3b3-4498-8926-6712e572dc97/4Ik7UCiccn.json"
#Previously user_defined function 
lottie_json = load_lottie_url("https://lottie.host/a668460c-a3b3-4498-8926-6712e572dc97/4Ik7UCiccn.json")
with st.sidebar:
    if lottie_json:
        st_lottie(lottie_json, height=130)
    else:
        st.write("Lottie animation not found.")

    opt=option_menu("Navigation", ["Home", "Data Analysis", "Data Visualization", "Feedback"],icons=["house", "bar-chart", "graph-up", "chat-left-text"])
    # st.image("phone.gif",width=200)

#---------------------------------------HOME SECTION------------------------------------
if opt=="Home":
    st.title("🛒 Ecommerce Analysis Dashboard")
    st.subheader("🧩 Project Overview:")
    st.write("""
    The **Ecommerce Analysis** System is a data-driven web application developed using Python, Pandas, Streamlit, Matplotlib, Seaborn, and Plotly.
    It aims to analyze and visualize ecommerce sales data across different product categories, customer segments, geographic regions, and time periods.
    The system offers interactive dashboards and visual insights to help businesses:
    """)

#OBJECTIVES
    st.subheader("🎯 Objectives:")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        - **Analyze** overall sales performance and trends  
        - **Identify** top-selling products and underperforming categories  
        """)

    with col2:
        st.markdown("""
        - **Understand** customer purchase patterns and behavior  
        - **Provide** actionable insights for improving marketing, inventory, and operations  
        """)


#TECHNOLOGIES USED
    st.subheader("🔧 Technologies Used:")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
    - **Python**: For core data processing  
    - **Pandas**: For data manipulation  
    - **Matplotlib**: For static plots """)
        
    with col2:
        st.markdown("""
    - **Seaborn**: For statistical graphs  
    - **Plotly**: For interactive visualizations  
    - **Streamlit**: For web app development""")
        
# FEATURES
    st.subheader("📊 Key Features:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        - **State-wise Sales & Profit Analysis**: Identify high-performing and low-performing regions  
        - **Time-based Sales Trends**: Yearly and monthly breakdowns to spot seasonal patterns  
        - **Interactive Dashboards**: Dynamic charts and filters for deeper exploration  
        """)

    with col2:
        st.markdown("""
        - **Category & Segment Insights**: Evaluate product categories and customer segments  
        - **Data-driven Decision Support**: Insights to optimize marketing, inventory, and sales strategies  
        - **User-Friendly Interface**: Simple navigation and clean design for all users  
        """)


# #DEVELOPER
#     st.subheader("👩‍💻 Developer:")
#     st.markdown("""
    # **Developed by:** Geetanjally             
    # **Contact:** [geetanjallyrani22@gmail.com](mailto:geetanjallyrani22@gmail.com)
    # """)

#-----------------------------------DATA ANALYSIS---------------------------------------
elif opt=="Data Analysis":        
    st.title("📈 Data Analysis")
    st.write("Perform various data analysis here such as identifying trends, patterns, and comparing shoping trends across states or years.")

    def load_data():
        df = pd.read_csv("ecommerce_clean.csv",encoding="latin")
        return df
    df = load_data()

    tab1, tab2, tab3 ,tab4= st.tabs(
        ["🔍Sales Data Preview","📈 Sales Analysis", "📦 Product Analysis","👥 Customer Analysis"])
    with tab1:
        st.subheader("🔍 Sales Data Preview")
        st.dataframe(df)

        st.subheader("📌 Summary Statistics")
        st.write(df.describe())

        # Unique values
        years = sorted(df["Order Year"].unique())
        city = sorted(df["City"].unique())

        # Filters
        st.subheader("🎚 Filter Options")
        col1, col2 = st.columns(2)

        with col1:
            selected_year = st.selectbox("Select Year", ["All"] + years)
        with col2:
            selected_city = st.selectbox("Select City", ["All"] + city)

        
        # Filtered data
        filtered_df = df.copy()
        if selected_year != "All":
            filtered_df = filtered_df[filtered_df["Order Year"] == selected_year]
        if selected_city != "All":
            filtered_df = filtered_df[filtered_df["City"] == selected_city]

        st.subheader("📋 Filtered Data")
        st.dataframe(filtered_df, use_container_width=True)

        # Key Insights
        st.subheader("📊 Key Insights")
        print(filtered_df.columns)
        total_category = df["Category"].nunique()
        total_SubCategory =df["Sub-Category"].nunique()
        c1, c2= st.columns(2)
        c1.metric("Total Category", f"{total_category:,}")
        c2.metric("Total SubCategory", f"{total_SubCategory:,}")
    #SALES ANALYSIS
    with tab2:
    #max and min of sales and profit
        y = ["All"]+sorted(df["Order Year"].unique())
        r = ["Sales","Profit"]
        st.header("📊💸Sales & Profit")
        col1, col2 = st.columns(2)
        # key="year_selector_1"
        with col1:
            selected_y = st.selectbox("Select Year",y, key="year_selector_4")
        with col2:
            selected_r = st.selectbox("Select Profit/Sales",r,key="r_selector_1")

        # Filtered data
        if selected_y != "All":
            filtered_df = df[df["Order Year"] == selected_y]
        else:
            filtered_df = df.copy()

        if selected_r == "Sales":
            st.subheader("Max sales")
            # filtered_df = filtered_df[filtered_df["Order Year"] == selected_y]
            max_sales = filtered_df[["Order Month","Sales"]].loc[filtered_df['Sales'].idxmax()] #idxmax() provide index of max value
            st.write(max_sales)

            st.subheader("Min sales")
            min_sales = filtered_df[["Order Month","Sales"]].loc[filtered_df['Sales'].idxmin()]
            st.write(min_sales)

        if selected_r == "Profit":
            st.subheader("Max Profit")
            # filtered_df = filtered_df[filtered_df["Order Year"] == selected_y]
            max_profit = filtered_df[["Order Month","Profit"]].loc[filtered_df['Profit'].idxmax()] #idxmax() provide index of max value
            st.write(max_profit)

            st.subheader("Min Profit")
            min_profit = filtered_df[["Order Month","Profit"]].loc[filtered_df['Profit'].idxmin()]
            st.write(min_profit)

#PRODUCT ANALYSIS
    with tab3:
    #sales and profit on the basis of category
        y = ["All"]+sorted(df["Order Year"].unique())
        r = ["Sales","Profit"]
        st.header("Sales & Profit on the basis of Category")
        col1, col2 = st.columns(2)
        # key="year_selector_1"
        with col1:
            selected_y = st.selectbox("Select Year",y, key="year_selector_5")
        with col2:
            selected_r = st.selectbox("Select Profit/Sales",r,key="r_selector_2")

        # Filtered data
        if selected_y != "All":
            filtered_df = df[df["Order Year"] == selected_y]
        else:
            filtered_df = df.copy()

        if selected_r == "Sales":
            st.subheader("Category sales")
            category_sales = filtered_df.groupby("Category")["Sales"].sum()
            st.write(category_sales)

            max_category=category_sales.idxmax()
            cat_max=category_sales.loc[max_category] #idxmax() provide index of max value
            st.write("Category: ",max_category,", Maximum Sales: ",cat_max)

            min_category=category_sales.idxmin()
            cat_min=category_sales.loc[min_category]
            st.write("Category: ",min_category,", Minimum Sales: ",cat_min)

        if selected_r == "Profit":
            st.subheader("Category Profit")
            category_profit= filtered_df.groupby("Category")["Profit"].sum()
            st.write(category_profit)
            
            max_category=category_profit.idxmax()
            cat_max=category_profit.loc[max_category] #idxmax() provide index of max value
            st.write("Category: ",max_category,", Maximum Sales: ",cat_max)

            min_category=category_profit.idxmin()
            cat_min=category_profit.loc[min_category] #idxmax() provide index of max value
            st.write("Category: ",min_category,", Minimum Sales: ",cat_min)

    #sales and profit on the basis of subcategory
        y = ["All"]+sorted(df["Order Year"].unique())
        r = ["Sales","Profit"]
        st.header("Sales & Profit on the basis of SubCategory")
        col1, col2 = st.columns(2)
        # key="year_selector_1"
        with col1:
            selected_y = st.selectbox("Select Year",y, key="year_selector_6")
        with col2:
            selected_r = st.selectbox("Select Profit/Sales",r,key="r_selector_3")

        # Filtered data
        if selected_y != "All":
            filtered_df = df[df["Order Year"] == selected_y]
        else:
            filtered_df = df.copy()

        if selected_r == "Sales":
            st.subheader("SubCategory Sales")
            subcategory_sales = filtered_df.groupby("Sub-Category")["Sales"].sum()
            st.write(subcategory_sales)

            max_subcategory=subcategory_sales.idxmax()#idxmax() provide index of max value
            subcat_max_value=subcategory_sales.loc[max_subcategory]
            st.write("SubCategory: ",max_subcategory,", Maximum Sales: ",subcat_max_value)

            min_subcategory=subcategory_sales.idxmin()#idxmax() provide index of max value
            subcat_min_value=subcategory_sales.loc[min_subcategory]
            st.write("SubCategory: ",min_subcategory,", Minimum Sales: ",subcat_min_value)

        if selected_r == "Profit":
            st.subheader("SubCategory Profit")
            subcategory_profit = filtered_df.groupby("Sub-Category")["Profit"].sum() #idxmax() provide index of max value
            st.write(subcategory_profit)

            max_subcategory=subcategory_profit.idxmax()#idxmax() provide index of max value
            subcat_max_value=subcategory_profit.loc[max_subcategory]
            st.write("SubCategory: ",max_subcategory,", Profit: ",subcat_max_value)

            min_subcategory=subcategory_profit.idxmin()#idxmax() provide index of max value
            subcat_min_value=subcategory_profit.loc[min_subcategory]
            st.write("SubCategory: ",min_subcategory,", Loss: ",subcat_min_value)

    #sales and profit on the basis of customer segment
        y = ["All"]+sorted(df["Order Year"].unique())
        r = ["Sales","Profit"]
        st.header("Sales & Profit on the basis of Customer Segment")
        col1, col2 = st.columns(2)
        # key="year_selector_1"
        with col1:
            selected_y = st.selectbox("Select Year",y, key="year_selector_7")
        with col2:
            selected_r = st.selectbox("Select Profit/Sales",r,key="r_selector_4")

        # Filtered data
        if selected_y != "All":
            filtered_df = df[df["Order Year"] == selected_y]
        else:
            filtered_df = df.copy()

        if selected_r == "Sales":
            st.subheader("Max sales")
            df_segment=filtered_df.groupby("Segment")["Sales"].sum()
            st.write(df_segment)

            segment=df_segment.idxmax()
            df_max=df_segment.loc[segment]
            st.write("Customer Segment: ",segment,", max_sale: ",df_max)

            segment=df_segment.idxmin()
            df_min=df_segment.loc[segment]
            st.write("Customer Segment: ",segment,", min_sale: ",df_min)


        if selected_r == "Profit":
            st.subheader("Max Profit")
            df_segment=filtered_df.groupby("Segment")["Profit"].sum()
            st.write(df_segment)

            segment=df_segment.idxmax()
            df_max=df_segment.loc[segment]
            st.write("Customer Segment: ",segment,", Profit: ",df_max)

            segment=df_segment.idxmin()
            df_min=df_segment.loc[segment]
            st.write("Customer Segment: ",segment,", Loss: ",df_min)

    #IMPACT ANALYSIS       
    with tab4:
    #High Risk products
        st.header("High Risk Products")
        sales_per_customer = df.groupby("Sub-Category")[["Sales","Profit"]].sum().reset_index()
        risk_pr= sales_per_customer.sort_values(by="Sales", ascending=False)
        st.write(risk_pr)

    #Top 5 loyal customers
        st.header("Loyal Customer & Customer Value")
        r = ["Customer Loyalty","Customer Value"]
        val = st.selectbox("Select Customer Loyalty/Customer Value",r)
        filtered_df = df.copy()
        frequency_purchase=df["Customer ID"].value_counts().reset_index()
        frequency_purchase.columns=["Customer ID", "Frequency"]
        # frequency_purchase
        sales_per_customer = df.groupby("Customer ID")["Sales"].sum().reset_index()
        sales_per_customer.columns = ["Customer ID", "Total Sales"]

        if val=="Customer Loyalty":
            st.header("Top 5 loyal Customer")
            customer_loyalty=pd.merge(frequency_purchase,sales_per_customer,on="Customer ID")
            customer_loyalty=customer_loyalty.sort_values(by="Frequency",ascending=False)
            st.write(customer_loyalty.head(5))

        if val=="Customer Value":
            st.header("Top 5 Customer Value")
            customer_value=pd.merge(frequency_purchase,sales_per_customer,on="Customer ID")
            customer_value=customer_value.sort_values(by="Total Sales",ascending=False)
            st.write(customer_value.head(5))

#------------------------------------DATA VISUALIZATION------------------------------------
elif opt=="Data Visualization":
    st.title("📊 Data Visualization")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 Sales Charts", "📦 Category Charts", "🗺 SubCategory Charts", "👥 Customer Segment Charts", "📉 Impact Analysis"])
    with tab1:
        #YEAR WISE REPRESENTATION
        st.subheader("Orders By Year")
        df=pd.read_csv("ecommerce_clean.csv")
        year_counts = df["Order Year"].value_counts().reset_index()
        year_counts.columns = ["Year", "Count"]
        fig = px.pie(year_counts, names="Year", values="Count", width=650,height=500)
        st.plotly_chart(fig)

        # SALES VS PROFIT OF ONE SPECIFIC YEAR  
        # Unique values
        years = ["All"]+sorted(df["Order Year"].unique())
        rep = ["Bar Chart","Line Chart"]
        # Filters
        st.subheader("Sales VS Profit")
        col1, col2 = st.columns(2)

        with col1:
            selected_year = st.selectbox("Select Year", years)
        with col2:
            selected_rep = st.selectbox("Select Visualization way",rep)

        
        # Filtered data
        if selected_year != "All":
            filtered_df = df[df["Order Year"] == selected_year]
        else:
            filtered_df = df.copy()

        # filtered_df = df.copy()
        if selected_rep == "Bar Chart":
            monthly_summary = filtered_df.groupby("Order Month")[["Sales", "Profit"]].sum().reset_index()
            month_order = ["January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"]
            fig = px.bar(
                monthly_summary,
                x="Order Month",
                y=["Sales", "Profit"],
                title=f"{selected_year} Monthly Sales vs Profit",
                barmode="group",  
                category_orders={"Order Month": month_order},
                width=900,height=500)
            fig.update_layout(xaxis_title="Month", yaxis_title="Amount", legend_title="Metric")
            st.plotly_chart(fig)

        if selected_rep == "Line Chart":
            monthly_summary = filtered_df.groupby("Order Month")[["Sales", "Profit"]].sum().reset_index()
            month_order = ["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"]
            fig = px.line(monthly_summary, x="Order Month", y=['Sales', 'Profit'],markers= True,
                        title=f"{selected_year} Monthly Sales Trend",
                        labels={"Sales": "Total Sales", "Order Month": "Month"})
            fig.update_layout(xaxis_tickangle=-45)  
            st.plotly_chart(fig)

        #SALES AND PROFIT INDIVIDUALLY
        y = ["All"]+sorted(df["Order Year"].unique())
        r = ["Sales","Profit"]
        col1, col2 = st.columns(2)
        # key="year_selector_1"
        with col1:
            selected_y = st.selectbox("Select Year",y, key="year_selector_1")
        with col2:
            selected_r = st.selectbox("Select Profit/Sales",r)

        #filtered dataset
        if selected_y!="All":
            filtered_df=df[df["Order Year"] == selected_y]
        else:
            filtered_df=df.copy()
    
        if selected_r == "Sales":
            st.subheader("Sales")
            mp = filtered_df.groupby("Order Month")["Sales"].sum().reset_index()
            month_order = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]
            mp["Order Month"]=pd.Categorical(mp["Order Month"],categories=month_order, ordered=True)
            mp=mp.sort_values("Order Month")
            fig = px.line(mp, x="Order Month", y="Sales",markers= True,
                        title=f"{selected_y} Monthly Sales Trend",
                        labels={"Sales": "Total Sales", "Order Month": "Month"})

            fig.update_layout(xaxis_tickangle=-45)  
            st.plotly_chart(fig)
        
        if selected_r == "Profit":
            st.subheader("Profit")
            mp = filtered_df.groupby("Order Month")["Profit"].sum().reset_index()
            month_order = ["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"]
            mp["Order Month"]=pd.Categorical(mp["Order Month"],categories=month_order, ordered=True)
            mp=mp.sort_values("Order Month")
            fig = px.line(mp, x="Order Month", y="Profit",markers= True,
                        title=f"{selected_y} Monthly Profit Trend",
                        labels={"Profit": "Total Profit", "Order Month": "Month"})

            fig.update_layout(xaxis_tickangle=-45)  
            st.plotly_chart(fig)

    with tab2:
        #Product category based analysis
        st.header("Product Category Based Analysis")
        df_category=df["Category"].value_counts().reset_index()
        df_category.columns=["Category","Count"]
        # df_category.columns
        fig=px.pie(df_category,names="Category",values="Count",width=650,height=500)
        st.plotly_chart(fig)

    #Profit acc to Category
        r = ["Sales","Profit"]
        selected_r = st.selectbox("Select Profit/Sales",r,key="r_selector_5")
        st.header(f"{selected_r} according to Category")
        if selected_r == "Sales":
            mp=df.groupby("Category")["Sales"].sum().reset_index()
            fig=px.bar(mp,x="Category",y="Sales")
            st.plotly_chart(fig)

        if selected_r == "Profit":
            mp=df.groupby("Category")["Profit"].sum().reset_index()
            fig=px.bar(mp,x="Category",y="Profit")
            st.plotly_chart(fig)


    #Product Category of one specific year
        y = ["All"]+sorted(df["Order Year"].unique())
        r = ["Sales","Profit"]
        col1, col2 = st.columns(2)
        # key="year_selector_1"
        with col1:
            selected_y = st.selectbox("Select Year",y, key="year_selector_2")
        with col2:
            selected_r = st.selectbox("Select Profit/Sales",r,key="year_selected_6")
        st.subheader(f"{selected_y} Profit according to Category")

        if selected_y != "All":
            filtered_df = df[df["Order Year"] == selected_y]
        else:
            filtered_df = df.copy()
        if selected_r == "Sales":
            mp=filtered_df.groupby("Category")["Sales"].sum().reset_index()
            fig=px.bar(mp,x="Category",y="Sales",title="Sales according to Category in 2017")
            st.plotly_chart(fig)
        if selected_r == "Profit":
            mp=filtered_df.groupby("Category")["Profit"].sum().reset_index()
            fig=px.bar(mp,x="Category",y="Profit",title="Profit according to Category in 2017")
            st.plotly_chart(fig)

    with tab3:
    #SUBCATEGORY ANALYSIS
        st.header("Subcategory Analysis")
        df_category=df["Sub-Category"].value_counts().reset_index()
        df_category.columns=["Sub-Category","Count"]
        # df_category.columns
        fig=px.pie(df_category,names="Sub-Category",values="Count",width=700,height=500)
        st.plotly_chart(fig)

    #Product SubCategory of all specific year
        r = ["Sales","Profit"]
        selected_r = st.selectbox("Select Profit/Sales",r,key="year_selected_7")
        if selected_r == "Sales":
            mp=df.groupby("Sub-Category")["Sales"].sum().reset_index()
            fig=px.bar(mp,x="Sub-Category",y="Sales",title="Sales according to Sub-Category ")
            st.plotly_chart(fig)
        if selected_r == "Profit":
            mp=df.groupby("Sub-Category")["Profit"].sum().reset_index()
            fig=px.bar(mp,x="Sub-Category",y="Profit",title="Profit according to Sub-Category ")
            st.plotly_chart(fig)

    #Product SubCategory of one specific year
        y =["All"] + sorted(df["Order Year"].unique())
        r = ["Sales","Profit"]
        col1,col2 = st.columns(2)
        with col1:
            selected_y = st.selectbox("Select Year",y, key="year_selector_3")
        with col2:
            selected_r = st.selectbox("Select Profit/Sales",r,key="year_selected_8")
        
        if selected_y != "All":
            filtered_df = df[df["Order Year"] == selected_y]
        else:
            filtered_df = df.copy()

        if selected_r == "Sales":
            st.subheader(f"{selected_r} according to SubCategory")
            mp=filtered_df.groupby("Sub-Category")["Sales"].sum().reset_index()
            fig = px.bar(mp,x="Sub-Category",y="Sales",title="Sales according to Sub-Category of 2017")
            st.plotly_chart(fig)

        if selected_r == "Profit":
            st.subheader(f"{selected_r} according to SubCategory")
            mp=filtered_df.groupby("Sub-Category")["Profit"].sum().reset_index()
            fig = px.bar(mp,x="Sub-Category",y="Profit",title="Profit according to Sub-Category of 2017")
            st.plotly_chart(fig) 

    with tab4:
    #Customer Segement
        st.header("Customer Segement")
        c_segment=df["Segment"].value_counts().reset_index()
        c_segment.columns=["Segment","count"]
        # c_segment
        fig= px.pie(c_segment,names="Segment",values="count",width=650,height=450)
        st.plotly_chart(fig)

    #Customer Segment sales analysis of all year
        st.header("Customer Segment Sales Analysis")
        df_sales = df.groupby(["Order Year", "Segment"])["Sales"].sum().reset_index()
        # df_sales
        fig=px.line(df_sales,x="Order Year",y="Sales",color="Segment",markers=True)
        st.plotly_chart(fig)

    #Customer Segment Sales Analysis of per year
        y =["All"] + sorted(df["Order Year"].unique())
        r = ["Sales","Profit"]
        col1,col2 = st.columns(2)
        with col1:
            selected_y = st.selectbox("Select Year",y, key="year_selector_4")
        with col2:
            selected_r = st.selectbox("Select Profit/Sales",r,key="r_selected_9")
        
        if selected_y != "All":
            filtered_df = df[df["Order Year"] == selected_y]
        else:
            filtered_df = df.copy()

        if selected_r == "Sales":
            st.subheader("Sales according to SubCategory")
            df_sales=filtered_df.groupby("Segment")["Sales"].sum().reset_index()
            fig = px.bar(df_sales,x="Segment",y="Sales")
            st.plotly_chart(fig)

        if selected_r == "Profit":
            st.subheader("Profit according to SubCategory")
            df_sales=filtered_df.groupby("Segment")["Profit"].sum().reset_index()
            fig = px.bar(df_sales,x="Segment",y="Profit")
            st.plotly_chart(fig)



    with tab5:
    #Sales to profit ratio of each specific year
        df_ratio=df["Profit"].sum()/df["Sales"].sum()
        st.header("Sales to profit ratio of each specific year")
        df_year=df.groupby("Order Year")[["Sales","Profit"]].sum().reset_index()
        df_year["Ratio"]=df_year["Profit"]/df_year["Sales"]
        fig=px.bar(df_year,x="Order Year",y="Ratio")
        st.plotly_chart(fig)


    #Sales by US State
        st.header("📦 Sales by US State with Hover Details")
        state_summary = df.groupby("State")[["Sales", "Profit"]].sum().reset_index()
        fig = px.choropleth(state_summary,locations=state_summary["State"],
                        locationmode="USA-states",
                        color=state_summary["Sales"],
                        scope="usa",
                        color_continuous_scale="Viridis",
                        labels={"color": "Total Sales"},
                        hover_name=state_summary["State"],
                        hover_data={
                            "Sales": True,
                            "Profit": True,
                            "State": False 
                        }, )
        fig.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
        st.plotly_chart(fig)

    #Shipping mode impact
        st.header("Sales and Profit by Shipping Mode")
        monthly_summary = df.groupby("Ship Mode")[["Sales", "Profit"]].sum().reset_index()
        fig = px.bar(monthly_summary, 
                    x="Ship Mode", 
                    y=["Sales", "Profit"], 
                    barmode="group",
                    labels={"value": "Amount", "variable": "Metric", "Ship Mode": "Shipping Mode"})
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig)

    #Customer Loyalty vs Value (Highlighting Top 5 Loyal Customers)
        st.header("Customer Loyalty vs Value (Highlighting Top 5 Loyal Customers)")
        frequency_purchase=df["Customer ID"].value_counts().reset_index()
        frequency_purchase.columns=["Customer ID", "Frequency"]
        # frequency_purchase
        sales_per_customer = df.groupby("Customer ID")["Sales"].sum().reset_index()
        sales_per_customer.columns = ["Customer ID", "Total Sales"]
        # sales_per_customer
        customer_loyalty=pd.merge(frequency_purchase,sales_per_customer,on="Customer ID")
        
        # Customer Loyalty
        customer_loyalty=customer_loyalty.sort_values(by="Frequency",ascending=False)
        customer_loyalty.head(10)
        
        #Customer Value
        customer_value=pd.merge(frequency_purchase,sales_per_customer,on="Customer ID")
        customer_value=customer_value.sort_values(by="Total Sales",ascending=False)
        customer_value.head(10)
        top_loyal = customer_value.sort_values(by="Total Sales", ascending=False).head(5)
        top_ids = top_loyal["Customer ID"].tolist()
        plot_df=customer_value.sort_values(by="Total Sales", ascending=False).head(50).copy()
        plot_df["Customer Type"]=customer_value["Customer ID"].apply(lambda x: "Top 5" if x in top_ids else "Others")
        fig = px.scatter(plot_df,  x="Frequency", 
                        y="Total Sales", 
                        color="Customer Type",
                        size="Total Sales",
                        hover_name="Customer ID")
        st.plotly_chart(fig)

    #Discount Impact Analysis
        st.header("Discount Impact Analysis")
        df["Discount"].value_counts()
        fig=px.scatter(df,x="Discount",y="Profit")
        st.plotly_chart(fig)

#--------------------------------------FEEDBACK---------------------------------------------
elif opt == 'Feedback':
    st.title("📝 Feedback")
    st.write("We value your feedback! Please share your thoughts below.")

    name = st.text_input("Your Name:")
    email = st.text_input("Your Email:")
    feedback = st.text_area("Your Feedback:")

    if st.button("Submit Feedback"):
        if not name or not email or not feedback:
            st.error("Please fill in all the fields.")
        else:
            if reg((name, email, feedback)):
                st.success("Thank you for your valuable feedback!")
                st.toast("Feedback saved successfully!")
            else:
                st.error("Something went wrong while saving your feedback.")

# ---------------------- FOOTER ----------------------

st.markdown(
    """
    <hr style="margin-top: 50px;"/>
    <div style='text-align: center; font-size: 14px; color: gray;'>
        Developed by: <b>Geetanjally</b> | Contact: <a href='mailto:geetanjallyrani22@gmail.com'>geetanjallyrani22@gmail.com</a>
    </div>
    """,
    unsafe_allow_html=True

)



