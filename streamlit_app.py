import streamlit as st
import requests
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input("Name on Smoothie:")

session = get_active_session()

st.write("The name on the order will be:", name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(
    col("FRUIT_NAME"),
    col("SEARCH_ON")
)

pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    pd_df["FRUIT_NAME"].tolist(),
    max_selections=5
)

if ingredients_list:
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ", "

        search_on = pd_df.loc[
            pd_df["FRUIT_NAME"] == fruit_chosen, "SEARCH_ON"
        ].iloc[0]

        st.write("The search value for", fruit_chosen, "is", search_on)

        st.subheader(f"{fruit_chosen} Nutrition Information")

        smoothiefroot_response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{search_on}"
        )

        if smoothiefroot_response.status_code == 200:
            st.dataframe(
                data=smoothiefroot_response.json(),
                use_container_width=True
            )
        else:
            st.error(f"Failed to fetch data for {fruit_chosen}")

# Optional fixed example call
smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

if smoothiefroot_response.status_code == 200:
    st.text(str(smoothiefroot_response.json()))
    st.dataframe(
        data=smoothiefroot_response.json(),
        use_container_width=True
    )
