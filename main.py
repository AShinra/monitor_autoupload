from datetime import date, datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId


def connect_to_mongo():
    client = MongoClient('mongodb://admin:q8vm5dz-h29piX%3FMo%26%3ClO4e0zn@mongodb4:27017,arbiter:27017/zeno_db?authSource=admin&replicaSet=rs1')
    db = client["zeno_db"]
    collection = db["articles_app_article"]
    return collection

def write_to_file(file_name, new_data):
    with open(file_name, "a") as file:
        file.write(f'{new_data}\n')


if __name__ == '__main__':

    # get collection from mongodb
    collection = connect_to_mongo()

    # get date today
    _date = date.today()

    print(f'Generated as of {datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}')

    file_name = f'timelogs.txt'
    write_to_file(file_name, f'\nGenerated as of {datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}')

    # generate dates from the range i
    for i in range (0, 6):
        new_date = _date - timedelta(days=i)
        _month= new_date.month
        _day= new_date.day
        _year = new_date.year

        # generate query
        query = {
        "created_by_id": ObjectId("619f0998a834a290ce4ef787"),
        "media_source.media_source_type_flag": "web",
        "date_publish": {
            "$gte": datetime(_year, _month, _day-1, 16, 0, 0),
            "$lt": datetime(_year, _month, _day, 16, 0, 0)
        }}

        # Count documents matching the query
        count = collection.count_documents(query)
        
        # st.write(f"{new_date} ==>> {count} Articles")
        print(f"{new_date} ==>> {count} Articles")
        new_data = f"{new_date} ==>> {count} Articles"
        write_to_file(file_name, new_data)