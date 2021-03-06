import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError


streamlit.title ("My Parents New Healthy Diner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# pick list to select the fruits to include
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#display the table on the page

streamlit.dataframe(fruits_to_show)

# new function definition
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)    
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# new Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?', 'kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)    
    streamlit.dataframe(back_from_function)
except URLError as e:
      streamlit.error()

#streamlit.write('The user entered', fruit_choice)
#streamlit.text(fruityvice_response.json()) -- commenting

# format the json and normalize it
#fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display ont he screen
#streamlit.dataframe(fruityvice_normalized)

# don't run anything past here while we troubleshoot
#streamlit.stop() --commenting to DEBUG

streamlit.header("The fruit load list contains:")
#snowflake related functions
def get_fruit_laod_list():
        with my_cnx.cursor() as my_cur:
             my_cur.execute("SELECT * from fruit_load_list")
             return my_cur.fetchall()
        
# Adda  button to load the fruit
if streamlit.button('Get Fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
    
#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_rows = my_cur.fetchall()
#streamlit.header("The Fruit load list contains:")
#streamlit.dataframe(my_data_rows)


# new Section to add a selection
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('" + my_data_rows  +"')")
        return "Thanks for adding " + new_fruit
    
add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
#streamlit.write('Thanks for adding ', add_my_fruit)

#my_cur.execute("insert into fruit_load_list values ('from streamlit')")
