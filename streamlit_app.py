# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie:cup_with_straw:")
st.write(
  """choose the fruits you want in your custom smoothie
  """
)

name_on_order = st.text_input("Name on Smoothie")
st.write("The name on the Smoothie will be", name_on_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options")
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'choose upto 5 ingredients:',my_dataframe,
    max_selections = 5
)
if ingredients_list:
    st.write("You selected:", ingredients_list)

ingredients_string = ''
for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen+' '

st.write("ingredients_string:", ingredients_string)    

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """' ,'"""+name_on_order+"""')"""

st.write(my_insert_stmt)
#st.stop()
time_to_insert = st.button('submit order')
if time_to_insert:
#if ingredients_string:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
cnx=st.connection("snowflake")    
session = cnx.session()  
