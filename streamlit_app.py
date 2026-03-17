import streamlit as st
from snowflake.snowpark.functions import col


st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
cnx = st.connection("snowflake")
session = cnx.session()

fruit_rows = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME")).collect()
fruit_list = [row["FRUIT_NAME"] for row in fruit_rows]

ingredients_list = st.multiselect("Choose up to 5 ingredients:", fruit_list, max_selections=5)

time_to_insert = st.button("Submit Order")

if time_to_insert:
    if not name_on_order:
        st.error("Please enter a name.")
    elif not ingredients_list:
        st.error("Please choose at least one ingredient.")
    else:
        ingredients_string = ", ".join(ingredients_list)

        insert_sql = """
            insert into smoothies.public.orders(ingredients, name_on_order)
            values (?, ?)
        """

        session.sql(insert_sql, params=[ingredients_string, name_on_order]).collect()
        st.success("Your Smoothie is ordered!", icon="✅")
import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data= smoothiefroot_response.json(), use_container_width= True)
