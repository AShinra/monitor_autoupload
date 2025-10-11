import streamlit as st
from datetime import date, datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('mongodb://admin:q8vm5dz-h29piX%3FMo%26%3ClO4e0zn@mongodb4:27017,arbiter:27017/zeno_db?authSource=admin&replicaSet=rs1')
db = client["zeno_db"]
collection = db["articles_app_article"]

_date = date.today()
st.write(f'Generated as of {datetime.now().strftime("%I:%M %p")}')
for i in range (0, 6):
    new_date = _date - timedelta(days=i)
    _month= new_date.month
    _day= new_date.day
    _year = new_date.year

    query = {
    "created_by_id": ObjectId("619f0998a834a290ce4ef787"),
    "media_source.media_source_type_flag": "web",
    "date_publish": {
        "$gte": datetime(_year, _month, _day-1, 16, 0, 0),
        "$lt": datetime(_year, _month, _day, 16, 0, 0)
    }}

    # Count documents matching the query
    count = collection.count_documents(query)

    
    st.write(f"{new_date} ==>> {count} Articles")



# st.write(f'month {_date.month}')
# st.write(f'day {_date.day}')
# st.write(f'year {_date.year}')
# st.write(f'time {datetime.now().strftime("%I:%M %p")}')




# selected_date = st.date_input(
#     label='Select a Date',
#     value=date.today()
# )



# connect to mongodb
# exit()
# client = MongoClient('mongodb://admin:q8vm5dz-h29piX%3FMo%26%3ClO4e0zn@mongodb4:27017,arbiter:27017/zeno_db?authSource=admin&replicaSet=rs1')
# db = client["zeno_db"]
# collection = db["articles_app_article"]
# # st.write(collection.count_documents({}))

# # Define query
# query = {
#     "created_by_id": ObjectId("619f0998a834a290ce4ef787"),
#     "media_source.media_source_type_flag": "web",
#     "date_publish": {
#         "$gte": datetime(2025, 10, 9, 16, 0, 0),
#         "$lt": datetime(2025, 10, 10, 16, 0, 0)
#     }
# }

# # Count documents matching the query
# count = collection.count_documents(query)

# st.write(f"Number of matching documents: {count}")


