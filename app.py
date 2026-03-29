import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Victoria Gallardo", layout="wide")

df = pd.read_csv("airbnb.csv")
df.columns = [c.strip().replace(";;", "") for c in df.columns]

st.title("Victoria Gallardo")

st.sidebar.header("Filters")

selected_group = st.sidebar.multiselect(
    "Choose neighbourhood group",
    sorted(df["neighbourhood_group"].dropna().unique()),
    default=sorted(df["neighbourhood_group"].dropna().unique())
)

df_filtered = df[df["neighbourhood_group"].isin(selected_group)]

selected_room = st.sidebar.multiselect(
    "Choose room type",
    sorted(df_filtered["room_type"].dropna().unique()),
    default=sorted(df_filtered["room_type"].dropna().unique())
)

df_filtered = df_filtered[df_filtered["room_type"].isin(selected_room)]

min_price = int(df_filtered["price"].min())
max_price = int(df_filtered["price"].max())

selected_price = st.sidebar.slider(
    "Choose price range",
    min_price,
    max_price,
    (min_price, max_price)
)

df_filtered = df_filtered[
    (df_filtered["price"] >= selected_price[0]) &
    (df_filtered["price"] <= selected_price[1])
]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Listings", len(df_filtered))

with col2:
    st.metric("Average price", round(df_filtered["price"].mean(), 2))

with col3:
    st.metric("Average reviews/month", round(df_filtered["reviews_per_month"].mean(), 2))

tab1, tab2 = st.tabs(["Dashboard", "Extra analysis"])

with tab1:
    st.subheader("Relationship between listing type and number of people")

    fig1 = px.bar(
        df_filtered.groupby("room_type", as_index=False)["minimum_nights"].mean(),
        x="room_type",
        y="minimum_nights",
        color="room_type"
    )
    st.plotly_chart(fig1)

    col4, col5 = st.columns(2)

    with col4:
        st.subheader("Price by listing type")
        fig2 = px.bar(
            df_filtered.groupby("room_type", as_index=False)["price"].mean(),
            x="room_type",
            y="price",
            color="room_type"
        )
        st.plotly_chart(fig2)

    with col5:
        st.subheader("Reviews and price")
        fig3 = px.scatter(
            df_filtered,
            x="number_of_reviews",
            y="price",
            color="room_type"
        )
        st.plotly_chart(fig3)

with tab2:
    st.subheader("Top apartments by reviews per month")

    top_apartments = df_filtered.sort_values(
        "reviews_per_month",
        ascending=False
    ).head(10)

    fig4 = px.bar(
        top_apartments,
        x="name",
        y="reviews_per_month",
        color="neighbourhood_group"
    )
    st.plotly_chart(fig4)

    st.subheader("Filtered data")
    st.dataframe(df_filtered)
