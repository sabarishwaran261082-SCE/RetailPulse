# ==============================================
# RetailPulse AI Dashboard
# Part 1
# ==============================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path

CSV_MIME = "text/csv"

# Column name constants
CUSTOMER_ID = "Customer ID"

# File name constants
CUSTOMER_SEGMENTS_CSV = "customer_segments.csv"
SALES_FORECAST_CSV = "sales_forecast.csv"
LSTM_FORECAST_CSV = "lstm_forecast.csv"
INVENTORY_OPTIMIZATION_CSV = "inventory_optimization.csv"
CUSTOMER_CHURN_PREDICTIONS_CSV = "customer_churn_predictions.csv"

# -----------------------------------------------
# PAGE CONFIG
# -----------------------------------------------

st.set_page_config(
    page_title="RetailPulse",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------
# CUSTOM CSS
# -----------------------------------------------

st.markdown("""
<style>

.main{
    background:#F7F9FC;
}

.block-container{
    padding-top:2rem;
}

h1,h2,h3{
    color:#202124;
}

div[data-testid="metric-container"]{
    background:white;
    padding:18px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}

.sidebar .sidebar-content{
    background:#111827;
}

hr{
    margin-top:5px;
    margin-bottom:5px;
}

</style>
""",unsafe_allow_html=True)

# -----------------------------------------------
# PROJECT PATH
# -----------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

DATA_PATH = ROOT/"data"/"processed"

# -----------------------------------------------
# LOAD CSV
# -----------------------------------------------

@st.cache_data
def load_data(file_name):

    file_path = DATA_PATH/file_name

    if file_path.exists():
        return pd.read_csv(file_path)

    return None


retail = load_data("online_retail_processed.csv")
segments = load_data(CUSTOMER_SEGMENTS_CSV)
forecast = load_data(SALES_FORECAST_CSV)
lstm = load_data(LSTM_FORECAST_CSV)
inventory = load_data(INVENTORY_OPTIMIZATION_CSV)
churn = load_data(CUSTOMER_CHURN_PREDICTIONS_CSV)

st.write("Retail:", retail is not None)
st.write("Segments:", segments is not None)
st.write("Forecast:", forecast is not None)
st.write("LSTM:", lstm is not None)
st.write("Inventory:", inventory is not None)
st.write("Churn:", churn is not None)

# -----------------------------------------------
# CHECK DATA
# -----------------------------------------------

if retail is None:

    st.error("Processed Retail Dataset Not Found")
    st.stop()

# -----------------------------------------------
# DATE FORMAT
# -----------------------------------------------

retail["InvoiceDate"] = pd.to_datetime(retail["InvoiceDate"])

# -----------------------------------------------
# SIDEBAR
# -----------------------------------------------

st.sidebar.title("🛒 RetailPulse")

st.sidebar.markdown("---")

page = st.sidebar.radio(

    "Navigation",

    [

        "Dashboard",
        "Sales Analytics",
        "Customer Segmentation",
        "Demand Forecasting",
        "Inventory Optimization",
        "Customer Churn",
        "Reports"

    ]

)

st.sidebar.markdown("---")

st.sidebar.header("Filters")

country = st.sidebar.multiselect(

    "Country",

    sorted(retail["Country"].unique()),

    default=sorted(retail["Country"].unique())

)

year = st.sidebar.multiselect(

    "Year",

    sorted(retail["Year"].unique()),

    default=sorted(retail["Year"].unique())

)

month = st.sidebar.multiselect(

    "Month",

    sorted(retail["Month"].unique()),

    default=sorted(retail["Month"].unique())

)

# -----------------------------------------------
# FILTER DATA
# -----------------------------------------------

filtered = retail[

    (retail["Country"].isin(country)) &

    (retail["Year"].isin(year)) &

    (retail["Month"].isin(month))

]

# -----------------------------------------------
# DASHBOARD
# -----------------------------------------------

if page=="Dashboard":

    st.title("📊 Executive Dashboard")

    st.markdown("Business Intelligence Dashboard for RetailPulse")

    revenue = filtered["TotalPrice"].sum()

    customers = filtered[CUSTOMER_ID].nunique()

    orders = filtered["Invoice"].nunique()

    products = filtered["StockCode"].nunique()

    avg_order = revenue/orders if orders!=0 else 0

    quantity = filtered["Quantity"].sum()

    c1,c2,c3 = st.columns(3)

    c4,c5,c6 = st.columns(3)

    c1.metric(

        "💰 Revenue",

        f"${revenue:,.2f}"

    )

    c2.metric(

        "🧾 Orders",

        orders

    )

    c3.metric(

        "👤 Customers",

        customers

    )

    c4.metric(

        "📦 Products",

        products

    )

    c5.metric(

        "🛍 Items Sold",

        quantity

    )

    c6.metric(

        "💵 Avg Order",

        f"${avg_order:,.2f}"

    )

    st.markdown("---")

    left,right = st.columns(2)

    with left:

        monthly = (

            filtered

            .groupby("InvoiceMonth")["TotalPrice"]

            .sum()

            .reset_index()

        )

        fig = px.line(

            monthly,

            x="InvoiceMonth",

            y="TotalPrice",

            markers=True,

            title="Monthly Revenue Trend"

        )

        fig.update_layout(height=450)

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        country_sales=(

            filtered

            .groupby("Country")["TotalPrice"]

            .sum()

            .sort_values(ascending=False)

            .head(10)

            .reset_index()

        )

        fig=px.bar(

            country_sales,

            x="Country",

            y="TotalPrice",

            color="TotalPrice",

            title="Top Countries by Revenue"

        )

        fig.update_layout(height=450)

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.markdown("---")

    left,right = st.columns(2)

    with left:

        top_products=(

            filtered

            .groupby("Description")["TotalPrice"]

            .sum()

            .sort_values(ascending=False)

            .head(15)

            .reset_index()

        )

        fig=px.bar(

            top_products,

            x="TotalPrice",

            y="Description",

            orientation="h",

            color="TotalPrice",

            title="Top Revenue Products"

        )

        fig.update_layout(height=600)

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        hourly=(

            filtered

            .groupby("Hour")["TotalPrice"]

            .sum()

            .reset_index()

        )

        fig=px.area(

            hourly,

            x="Hour",

            y="TotalPrice",

            title="Hourly Revenue"

        )

        fig.update_layout(height=600)

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.markdown("---")

    st.subheader("Recent Transactions")

    st.dataframe(

        filtered.tail(20),

        use_container_width=True,

        hide_index=True

    )

# ==========================================================
# SALES ANALYTICS PAGE
# ==========================================================

elif page == "Sales Analytics":

    st.title("📈 Sales Analytics")

    st.markdown("Detailed analysis of retail sales performance.")

    # --------------------------------------------------
    # KPI ROW
    # --------------------------------------------------

    total_sales = filtered["TotalPrice"].sum()
    total_qty = filtered["Quantity"].sum()
    total_orders = filtered["Invoice"].nunique()
    avg_sales = total_sales / total_orders if total_orders else 0

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("💰 Total Sales", f"${total_sales:,.2f}")
    k2.metric("📦 Quantity Sold", f"{total_qty:,}")
    k3.metric("🧾 Orders", total_orders)
    k4.metric("💵 Avg Order Value", f"${avg_sales:,.2f}")

    st.divider()

    # --------------------------------------------------
    # MONTHLY SALES
    # --------------------------------------------------

    left, right = st.columns(2)

    with left:

        monthly_sales = (
            filtered
            .groupby(["Year", "Month"])["TotalPrice"]
            .sum()
            .reset_index()
        )

        monthly_sales["Month-Year"] = (
            monthly_sales["Year"].astype(str)
            + "-"
            + monthly_sales["Month"].astype(str)
        )

        fig = px.line(
            monthly_sales,
            x="Month-Year",
            y="TotalPrice",
            markers=True,
            title="Monthly Revenue"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        daily_sales = (
            filtered
            .groupby("Day")["TotalPrice"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            daily_sales,
            x="Day",
            y="TotalPrice",
            title="Revenue by Day of Month",
            color="TotalPrice"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # HOUR & WEEKDAY
    # --------------------------------------------------

    left, right = st.columns(2)

    with left:

        hour_sales = (
            filtered
            .groupby("Hour")["TotalPrice"]
            .sum()
            .reset_index()
        )

        fig = px.area(
            hour_sales,
            x="Hour",
            y="TotalPrice",
            title="Revenue by Hour"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        weekday_sales = (
            filtered
            .groupby("DayOfWeek")["TotalPrice"]
            .sum()
            .reset_index()
        )

        weekday_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        if weekday_sales["DayOfWeek"].dtype == object:
            weekday_sales["DayOfWeek"] = pd.Categorical(
                weekday_sales["DayOfWeek"],
                categories=weekday_order,
                ordered=True
            )
            weekday_sales = weekday_sales.sort_values("DayOfWeek")

        fig = px.bar(
            weekday_sales,
            x="DayOfWeek",
            y="TotalPrice",
            color="TotalPrice",
            title="Revenue by Weekday"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # WEEKEND VS WEEKDAY
    # --------------------------------------------------

    left, right = st.columns(2)

    with left:

        weekend = (
            filtered
            .groupby("IsWeekend")["TotalPrice"]
            .sum()
            .reset_index()
        )

        weekend["IsWeekend"] = weekend["IsWeekend"].replace({
            True: "Weekend",
            False: "Weekday"
        })

        fig = px.pie(
            weekend,
            names="IsWeekend",
            values="TotalPrice",
            title="Weekend vs Weekday Sales"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        quarter = (
            filtered
            .groupby("Quarter")["TotalPrice"]
            .sum()
            .reset_index()
        )

        fig = px.bar(
            quarter,
            x="Quarter",
            y="TotalPrice",
            color="Quarter",
            title="Quarterly Revenue"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # COUNTRY ANALYSIS
    # --------------------------------------------------

    left, right = st.columns(2)

    with left:

        country_sales = (
            filtered
            .groupby("Country")["TotalPrice"]
            .sum()
            .sort_values(ascending=False)
            .head(15)
            .reset_index()
        )

        fig = px.bar(
            country_sales,
            x="Country",
            y="TotalPrice",
            color="TotalPrice",
            title="Top 15 Countries"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        country_orders = (
            filtered
            .groupby("Country")["Invoice"]
            .nunique()
            .reset_index(name="Orders")
        )

        fig = px.scatter(
            country_orders,
            x="Country",
            y="Orders",
            size="Orders",
            color="Orders",
            title="Orders by Country"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # PRODUCT ANALYSIS
    # --------------------------------------------------

    left, right = st.columns(2)

    with left:

        top_products = (
            filtered
            .groupby("Description")["Quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(20)
            .reset_index()
        )

        fig = px.bar(
            top_products,
            x="Quantity",
            y="Description",
            orientation="h",
            color="Quantity",
            title="Top Selling Products"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        revenue_products = (
            filtered
            .groupby("Description")["TotalPrice"]
            .sum()
            .sort_values(ascending=False)
            .head(20)
            .reset_index()
        )

        fig = px.bar(
            revenue_products,
            x="TotalPrice",
            y="Description",
            orientation="h",
            color="TotalPrice",
            title="Highest Revenue Products"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # SALES HEATMAP
    # --------------------------------------------------

    st.subheader("📊 Sales Heatmap")

    heat = (
        filtered
        .pivot_table(
            values="TotalPrice",
            index="DayOfWeek",
            columns="Hour",
            aggfunc="sum",
            fill_value=0
        )
    )

    fig = px.imshow(
        heat,
        aspect="auto",
        title="Sales by Day & Hour"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # TRANSACTION TABLE
    # --------------------------------------------------

    st.subheader("📋 Sales Transactions")

    st.dataframe(
        filtered.sort_values("InvoiceDate", ascending=False),
        use_container_width=True,
        hide_index=True
    )

# ==========================================================
# CUSTOMER SEGMENTATION
# ==========================================================

elif page == "Customer Segmentation":

    st.title("👥 Customer Segmentation")

    if segments is None:
        st.error("customer_segments.csv not found.")
        st.stop()

    st.markdown(
        "Customer segmentation using **RFM Analysis** and **K-Means Clustering**."
    )

    # --------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------

    total_customers = segments[CUSTOMER_ID].nunique()

    avg_recency = segments["Recency"].mean()
    avg_frequency = segments["Frequency"].mean()
    avg_monetary = segments["Monetary"].mean()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Customers", total_customers)
    c2.metric("Avg Recency", f"{avg_recency:.1f}")
    c3.metric("Avg Frequency", f"{avg_frequency:.1f}")
    c4.metric("Avg Monetary", f"${avg_monetary:,.2f}")

    st.divider()

    # --------------------------------------------------
    # CLUSTER DISTRIBUTION
    # --------------------------------------------------

    left, right = st.columns(2)

    with left:

        cluster_count = (
            segments["Cluster"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        cluster_count.columns = ["Cluster", "Customers"]

        fig = px.bar(
            cluster_count,
            x="Cluster",
            y="Customers",
            color="Cluster",
            title="Customers per Cluster"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        fig = px.pie(
            cluster_count,
            names="Cluster",
            values="Customers",
            title="Cluster Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # RFM SCATTER
    # --------------------------------------------------

    left, right = st.columns(2)

    with left:

        fig = px.scatter(
            segments,
            x="Recency",
            y="Frequency",
            color="Cluster",
            size="Monetary",
            hover_data=[CUSTOMER_ID],
            title="Recency vs Frequency"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        fig = px.scatter(
            segments,
            x="Frequency",
            y="Monetary",
            color="Cluster",
            size="Monetary",
            hover_data=[CUSTOMER_ID],
            title="Frequency vs Monetary"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # 3D RFM CLUSTER
    # --------------------------------------------------

    fig = px.scatter_3d(
        segments,
        x="Recency",
        y="Frequency",
        z="Monetary",
        color="Cluster",
        hover_data=[CUSTOMER_ID],
        title="3D Customer Segmentation"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # RFM HISTOGRAMS
    # --------------------------------------------------

    left, center, right = st.columns(3)

    with left:

        fig = px.histogram(
            segments,
            x="Recency",
            nbins=30,
            color="Cluster",
            title="Recency Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with center:

        fig = px.histogram(
            segments,
            x="Frequency",
            nbins=30,
            color="Cluster",
            title="Frequency Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        fig = px.histogram(
            segments,
            x="Monetary",
            nbins=30,
            color="Cluster",
            title="Monetary Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # CLUSTER SUMMARY
    # --------------------------------------------------

    summary = (
        segments
        .groupby("Cluster")
        .agg(
            Customers=(CUSTOMER_ID, "count"),
            Avg_Recency=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Avg_Monetary=("Monetary", "mean")
        )
        .reset_index()
    )

    st.subheader("Cluster Summary")

    st.dataframe(
        summary.style.format({
            "Avg_Recency": "{:.2f}",
            "Avg_Frequency": "{:.2f}",
            "Avg_Monetary": "${:,.2f}"
        }),
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------
    # BOXPLOTS
    # --------------------------------------------------

    left, right = st.columns(2)

    with left:

        fig = px.box(
            segments,
            x="Cluster",
            y="Monetary",
            color="Cluster",
            title="Monetary by Cluster"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        fig = px.box(
            segments,
            x="Cluster",
            y="Frequency",
            color="Cluster",
            title="Frequency by Cluster"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # CUSTOMER TABLE
    # --------------------------------------------------

    st.subheader("Customer Segment Details")

    st.dataframe(
        segments.sort_values(
            ["Cluster", "Monetary"],
            ascending=[True, False]
        ),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇ Download Customer Segments",
        segments.to_csv(index=False),
        file_name=CUSTOMER_SEGMENTS_CSV,
        mime=CSV_MIME
    )
# ==========================================================
# DEMAND FORECASTING
# ==========================================================

elif page == "Demand Forecasting":

    st.title("📈 Demand Forecasting")

    st.markdown(
        "Sales forecasting using **Facebook Prophet** and **LSTM Neural Network**."
    )

    prophet_tab, lstm_tab = st.tabs(["📈 Prophet", "🤖 LSTM"])

    # =====================================================
    # PROPHET
    # =====================================================

    with prophet_tab:

        if forecast is None:

            st.warning(f"{SALES_FORECAST_CSV} not found.")

        else:

            st.subheader("Prophet Forecast")

            total_predictions = len(forecast)

            c1, c2, c3 = st.columns(3)

            c1.metric("Forecast Days", total_predictions)

            if "yhat" in forecast.columns:
                c2.metric(
                    "Average Forecast",
                    f"${forecast['yhat'].mean():,.2f}"
                )

                c3.metric(
                    "Maximum Forecast",
                    f"${forecast['yhat'].max():,.2f}"
                )

            # -------------------------
            # Forecast Line
            # -------------------------

            if {"ds", "yhat"}.issubset(forecast.columns):

                fig = px.line(
                    forecast,
                    x="ds",
                    y="yhat",
                    title="Prophet Forecast"
                )

                fig.update_traces(line_width=3)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            # -------------------------
            # Confidence Interval
            # -------------------------

            if {
                "ds",
                "yhat",
                "yhat_lower",
                "yhat_upper"
            }.issubset(forecast.columns):

                fig = go.Figure()

                fig.add_trace(

                    go.Scatter(

                        x=forecast["ds"],
                        y=forecast["yhat"],

                        name="Forecast"

                    )

                )

                fig.add_trace(

                    go.Scatter(

                        x=forecast["ds"],
                        y=forecast["yhat_upper"],

                        line={"width": 0},

                        showlegend=False

                    )

                )

                fig.add_trace(

                    go.Scatter(

                        x=forecast["ds"],
                        y=forecast["yhat_lower"],

                        fill='tonexty',

                        line={"width": 0},

                        name="Confidence Interval"

                    )

                )

                fig.update_layout(

                    title="Forecast Confidence Interval"

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

            st.subheader("Forecast Table")

            st.dataframe(

                forecast,

                use_container_width=True,

                hide_index=True

            )

            st.download_button(

                "⬇ Download Prophet Forecast",

                forecast.to_csv(index=False),

                file_name=SALES_FORECAST_CSV,

                mime=CSV_MIME

            )

    # =====================================================
    # LSTM
    # =====================================================

    with lstm_tab:

        if lstm is None:

            st.warning("lstm_forecast.csv not found.")

        else:

            st.subheader("LSTM Forecast")

            c1, c2, c3 = st.columns(3)

            c1.metric(

                "Predictions",

                len(lstm)

            )

            if "Predicted" in lstm.columns:

                c2.metric(

                    "Average Prediction",

                    f"${lstm['Predicted'].mean():,.2f}"

                )

                c3.metric(

                    "Maximum Prediction",

                    f"${lstm['Predicted'].max():,.2f}"

                )

            # --------------------------------

            if {

                "Actual",

                "Predicted"

            }.issubset(lstm.columns):

                fig = go.Figure()

                fig.add_trace(

                    go.Scatter(

                        y=lstm["Actual"],

                        mode="lines",

                        name="Actual"

                    )

                )

                fig.add_trace(

                    go.Scatter(

                        y=lstm["Predicted"],

                        mode="lines",

                        name="Predicted"

                    )

                )

                fig.update_layout(

                    title="Actual vs Predicted"

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

            # --------------------------------

            if "Predicted" in lstm.columns:

                fig = px.line(

                    lstm,

                    y="Predicted",

                    title="Predicted Sales"

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

            st.subheader("Prediction Table")

            st.dataframe(

                lstm,

                use_container_width=True,

                hide_index=True

            )

            st.download_button(

                "⬇ Download LSTM Forecast",

                lstm.to_csv(index=False),

                file_name="lstm_forecast.csv",

                mime=CSV_MIME

            )

    # =====================================================
    # COMPARISON
    # =====================================================

    st.divider()

    st.subheader("📊 Forecast Model Comparison")

    forecast_records_label = "Forecast Records"

    compare = pd.DataFrame({

        "Model": ["Prophet", "LSTM"],

        forecast_records_label: [

            len(forecast) if forecast is not None else 0,

            len(lstm) if lstm is not None else 0

        ]

    })

    fig = px.bar(

        compare,

        x="Model",

        y=forecast_records_label,

        color="Model",

        text=forecast_records_label,

        title=f"{forecast_records_label} Comparison"

    )

    st.plotly_chart(

        fig,

        use_container_width=True
    )

# ==========================================================
# INVENTORY OPTIMIZATION
# ==========================================================

elif page == "Inventory Optimization":

    st.title("📦 Inventory Optimization")

    if inventory is None:

        st.error("inventory_optimization.csv not found.")
        st.stop()

    st.markdown(
        "Inventory optimization using **ABC Analysis** and sales performance."
    )

    # -------------------------------------------------------
    # KPIs
    # -------------------------------------------------------

    total_products = inventory["StockCode"].nunique()

    total_revenue = inventory["TotalRevenue"].sum()

    total_quantity = inventory["TotalQuantity"].sum()

    avg_quantity = inventory["AvgQuantity"].mean()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Products", total_products)

    c2.metric("Revenue", f"${total_revenue:,.2f}")

    c3.metric("Units Sold", f"{total_quantity:,.0f}")

    c4.metric("Average Quantity", f"{avg_quantity:.2f}")

    st.divider()

    # -------------------------------------------------------
    # ABC DISTRIBUTION
    # -------------------------------------------------------

    left, right = st.columns(2)

    with left:

        abc_count = (

            inventory["ABC"]

            .value_counts()

            .reset_index()

        )

        abc_count.columns = ["Category", "Products"]

        fig = px.pie(

            abc_count,

            names="Category",

            values="Products",

            title="ABC Category Distribution"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        abc_revenue = (

            inventory

            .groupby("ABC")["TotalRevenue"]

            .sum()

            .reset_index()

        )

        fig = px.bar(

            abc_revenue,

            x="ABC",

            y="TotalRevenue",

            color="ABC",

            text_auto=".2s",

            title="Revenue by ABC Category"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    # -------------------------------------------------------
    # TOP REVENUE PRODUCTS
    # -------------------------------------------------------

    left, right = st.columns(2)

    with left:

        top_revenue = (

            inventory

            .sort_values(

                "TotalRevenue",

                ascending=False

            )

            .head(15)

        )

        fig = px.bar(

            top_revenue,

            x="TotalRevenue",

            y="Description",

            orientation="h",

            color="ABC",

            title="Top Revenue Products"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        top_quantity = (

            inventory

            .sort_values(

                "TotalQuantity",

                ascending=False

            )

            .head(15)

        )

        fig = px.bar(

            top_quantity,

            x="TotalQuantity",

            y="Description",

            orientation="h",

            color="ABC",

            title="Top Selling Products"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.divider()

    # -------------------------------------------------------
    # ORDERS ANALYSIS
    # -------------------------------------------------------

    left, right = st.columns(2)

    with left:

        inventory["BubbleQuantity"] = inventory["TotalQuantity"].abs() + 1

        fig = px.scatter(

             inventory,

             x="Orders",

             y="TotalRevenue",

             color="ABC",

             size="BubbleQuantity",

             hover_name="Description",

             title="Orders vs Revenue"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        inventory["BubbleOrders"] = inventory["Orders"].abs() + 1

        fig = px.scatter(

            inventory,

            x="AvgQuantity",

            y="TotalRevenue",

            color="ABC",

            size="BubbleOrders",

            hover_name="Description",

            title="Average Quantity vs Revenue"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    st.markdown(
        "Inventory optimization using **ABC Analysis** and sales performance."
    )

    # Clean negative values from returned/cancelled orders
    inventory["TotalQuantity"] = inventory["TotalQuantity"].abs()
    inventory["Orders"] = inventory["Orders"].abs()
    inventory["AvgQuantity"] = inventory["AvgQuantity"].abs()
    inventory["TotalRevenue"] = inventory["TotalRevenue"].abs()

    st.divider()

    # -------------------------------------------------------
    # RECOMMENDATION SUMMARY
    # -------------------------------------------------------

    st.subheader("📋 Inventory Recommendations")

    recommendation_summary = (

        inventory

        .groupby("Recommendation")

        .size()

        .reset_index(name="Products")

    )

    fig = px.bar(

        recommendation_summary,

        x="Recommendation",

        y="Products",

        color="Recommendation",

        title="Recommendation Distribution"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )

    st.divider()

    # -------------------------------------------------------
    # REORDER LIST
    # -------------------------------------------------------

    reorder = inventory[

        inventory["Recommendation"] == "Reorder Immediately"

    ]

    st.subheader("🚨 Products to Reorder")

    st.dataframe(

        reorder,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # -------------------------------------------------------
    # COMPLETE INVENTORY TABLE
    # -------------------------------------------------------

    st.subheader("Inventory Table")

    st.dataframe(

        inventory,

        use_container_width=True,

        hide_index=True

    )

    st.download_button(

        "⬇ Download Inventory Report",

        inventory.to_csv(index=False),

        file_name="inventory_optimization.csv",

        mime=CSV_MIME

    )
# ==========================================================
# CUSTOMER CHURN ANALYSIS
# ==========================================================

elif page == "Customer Churn":

    st.title("⚠ Customer Churn Analysis")

    if churn is None:

        st.error("customer_churn_predictions.csv not found.")
        st.stop()

    st.markdown(
        "Customer churn prediction using the trained Machine Learning model."
    )

    # -------------------------------------------------------
    # KPI CARDS
    # -------------------------------------------------------

    total_customers = len(churn)

    churned = len(churn[churn["Predicted"] == 1])

    retained = len(churn[churn["Predicted"] == 0])

    churn_rate = (
        churned / total_customers * 100
        if total_customers > 0
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Customers", total_customers)
    c2.metric("Predicted Churn", churned)
    c3.metric("Retained", retained)
    c4.metric("Churn Rate", f"{churn_rate:.2f}%")

    st.divider()

    # -------------------------------------------------------
    # CHURN DISTRIBUTION
    # -------------------------------------------------------

    left, right = st.columns(2)

    with left:

        churn_count = (
            churn["Predicted"]
            .value_counts()
            .reset_index()
        )

        churn_count.columns = ["Prediction", "Customers"]

        churn_count["Prediction"] = churn_count["Prediction"].replace(
            {
                0: "Retained",
                1: "Churn"
            }
        )

        fig = px.pie(
            churn_count,
            names="Prediction",
            values="Customers",
            title="Customer Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.bar(
            churn_count,
            x="Prediction",
            y="Customers",
            color="Prediction",
            text_auto=True,
            title="Churn Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # -------------------------------------------------------
    # RECENCY / FREQUENCY
    # -------------------------------------------------------

    if {
        "Recency",
        "Frequency",
        "Monetary"
    }.issubset(churn.columns):

        left, right = st.columns(2)

        with left:

            fig = px.scatter(
                churn,
                x="Recency",
                y="Frequency",
                color="Predicted",
                size="Monetary",
                hover_data=["Customer ID"],
                title="Recency vs Frequency"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with right:

            fig = px.scatter(
                churn,
                x="Frequency",
                y="Monetary",
                color="Predicted",
                size="Recency",
                hover_data=["Customer ID"],
                title="Frequency vs Monetary"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()

    # -------------------------------------------------------
    # HISTOGRAMS
    # -------------------------------------------------------

    if "Recency" in churn.columns:

        left, center, right = st.columns(3)

        with left:

            fig = px.histogram(
                churn,
                x="Recency",
                color="Predicted",
                nbins=30,
                title="Recency Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with center:

            fig = px.histogram(
                churn,
                x="Frequency",
                color="Predicted",
                nbins=30,
                title="Frequency Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with right:

            fig = px.histogram(
                churn,
                x="Monetary",
                color="Predicted",
                nbins=30,
                title="Monetary Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    st.divider()

    # -------------------------------------------------------
    # FEATURE SUMMARY
    # -------------------------------------------------------

    if {
        "Recency",
        "Frequency",
        "Monetary"
    }.issubset(churn.columns):

        summary = (
            churn
            .groupby("Predicted")
            .agg(
                Customers=("Customer ID", "count"),
                Avg_Recency=("Recency", "mean"),
                Avg_Frequency=("Frequency", "mean"),
                Avg_Monetary=("Monetary", "mean")
            )
            .reset_index()
        )

        summary["Predicted"] = summary["Predicted"].replace(
            {
                0: "Retained",
                1: "Churn"
            }
        )

        st.subheader("Customer Summary")

        st.dataframe(
            summary,
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # -------------------------------------------------------
    # MODEL METRICS
    # -------------------------------------------------------

    st.subheader("Model Performance")

    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric("Accuracy", "1.00")
    m2.metric("Precision", "1.00")
    m3.metric("Recall", "1.00")
    m4.metric("F1 Score", "1.00")
    m5.metric("ROC AUC", "1.00")

    st.info(
        "These values match the metrics obtained during model evaluation. "
        "If you retrain the model with different features, update them accordingly."
    )

    st.divider()

    # -------------------------------------------------------
    # CUSTOMER TABLE
    # -------------------------------------------------------

    st.subheader("Customer Predictions")

    st.dataframe(
        churn.sort_values(
            "Predicted",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇ Download Churn Predictions",
        churn.to_csv(index=False),
        file_name="customer_churn_predictions.csv",
        mime=CSV_MIME
    )
# ==========================================================
# REPORTS & DOWNLOAD CENTER
# ==========================================================

elif page == "Reports":
    st.success("REPORT PAGE VERSION 2")
    st.title("📑 Reports & Download Center")

    st.markdown(
        """
        Download all generated datasets and view a quick project summary.
        """
    )

    st.divider()

    # =====================================================
    # DATASET OVERVIEW
    # =====================================================

    st.subheader("📊 Dataset Overview")

    overview = pd.DataFrame({

        "Dataset": [

            "Processed Retail",
            "Customer Segments",
            "Sales Forecast",
            "LSTM Forecast",
            "Inventory",
            "Customer Churn"

        ],

        "Rows": [

            len(retail) if retail is not None else 0,
            len(segments) if segments is not None else 0,
            len(forecast) if forecast is not None else 0,
            len(lstm) if lstm is not None else 0,
            len(inventory) if inventory is not None else 0,
            len(churn) if churn is not None else 0

        ]

    })

    st.dataframe(
        overview,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =====================================================
    # DOWNLOAD BUTTONS
    # =====================================================

    st.subheader("⬇ Download Reports")

    c1, c2 = st.columns(2)

    with c1:

        if retail is not None:
            st.download_button(
                "Processed Retail Dataset",
                retail.to_csv(index=False),
                "online_retail_processed.csv",
                CSV_MIME
            )

        if forecast is not None:
            st.download_button(
                "Prophet Forecast",
                forecast.to_csv(index=False),
                "sales_forecast.csv",
                CSV_MIME
            )

        if inventory is not None:
            st.download_button(
                "Inventory Report",
                inventory.to_csv(index=False),
                "inventory_optimization.csv",
                CSV_MIME
            )

    with c2:

        if segments is not None:
            st.download_button(
                "Customer Segments",
                segments.to_csv(index=False),
                CUSTOMER_SEGMENTS_CSV,
                CSV_MIME
            )

        if lstm is not None:
            st.download_button(
                "LSTM Forecast",
                lstm.to_csv(index=False),
                "lstm_forecast.csv",
                CSV_MIME
            )

        if churn is not None:
            st.download_button(
                "Customer Churn",
                churn.to_csv(index=False),
                "customer_churn_predictions.csv",
                CSV_MIME
            )

    st.divider()

    # =====================================================
    # PROJECT SUMMARY
    # =====================================================

    st.subheader("📋 RetailPulse Summary")

    st.markdown("""
### Modules Completed

✅ ETL Pipeline

✅ Business Analytics

✅ Customer Segmentation

✅ Demand Forecasting

✅ Inventory Optimization

✅ Customer Churn Prediction

✅ Interactive Streamlit Dashboard
""")

    st.divider()

    # =====================================================
    # TECHNOLOGY STACK
    # =====================================================

    st.subheader("🛠 Technology Stack")

    tech = pd.DataFrame({

        "Technology": [

            "Python",
            "Pandas",
            "NumPy",
            "Scikit-Learn",
            "Prophet",
            "TensorFlow",
            "Plotly",
            "Streamlit"

        ],

        "Purpose": [

            "Programming",
            "Data Analysis",
            "Numerical Computing",
            "Machine Learning",
            "Forecasting",
            "Deep Learning",
            "Visualization",
            "Dashboard"

        ]

    })

    st.dataframe(
        tech,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # =====================================================
    # PROJECT STATISTICS
    # =====================================================

    st.subheader("📈 Project Statistics")

    s1, s2, s3, s4 = st.columns(4)

    s1.metric("Modules", "7")

    s2.metric("Charts", "25+")

    s3.metric("Datasets", "6")

    s4.metric("Dashboard", "Complete")

    st.divider()

    # =====================================================
    # ABOUT
    # =====================================================

    st.subheader("ℹ About RetailPulse")

    st.info(
        """
RetailPulse is an AI-powered Retail Analytics platform developed using
Python, Machine Learning, Deep Learning, Streamlit and Plotly.

Features include:

• Business Analytics

• Customer Segmentation

• Sales Forecasting

• Inventory Optimization

• Customer Churn Prediction

Designed as an end-to-end retail analytics solution.
"""
    )

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
    """
<div style='text-align:center;
font-size:15px;
color:gray;'>

Developed with ❤️ using Python • Streamlit • Plotly

<b>RetailPulse - AI Powered Retail Analytics Dashboard</b>

</div>
""",
unsafe_allow_html=True
)