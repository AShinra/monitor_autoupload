from datetime import date, datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId


def connect_to_mongo():
    client = MongoClient('mongodb://admin:q8vm5dz-h29piX%3FMo%26%3ClO4e0zn@mongodb4:27017,arbiter:27017/zeno_db?authSource=admin&replicaSet=rs1')
    db = client["zeno_db"]
    collection = db["articles_app_article"]
    return collection

def write_to_file(new_data):
    file_name = f'timelogs.txt'
    with open(file_name, "a") as file:
        file.write(f'{new_data}\n')

def connect_to_data():
    client = MongoClient('mongodb+srv://jonpuray:vYk9PVyQ7mQCn0Rj@cluster1.v4m9pq1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1')
    db = client['autoupload']
    collection = db['data']
    return collection

if __name__ == '__main__':

    # get collection from mongodb
    collection = connect_to_mongo()

    # get date today
    _date = date.today()

    print(f'Generated as of {datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}')

    write_to_file(f'\nOnline Automated PickUps Tracking')
    write_to_file(f'Generated as of {datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}')

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
        

        data_collection = connect_to_data()

        doc = data_collection.find_one(
            {'date':str(new_date)}
        )

        if doc:
            # get the last value and assign to old
            old_value = doc['value']['new']
            date_pre = doc['updated_at']

            # update the document
            data_collection.update_one(
                {'date':str(new_date)},
                {'$set':{
                    'value.old':old_value,
                    'value.new':count,
                    'updated_pre':date_pre,
                    'updated_at':f'{datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}'
                }})
        else:
            data = {
                'date':str(new_date),
                'value':{'old':0,'new':count},
                'updated_pre':'',
                'updated_at':f'{datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}'
            }

            data_collection.insert_one(data)
        
        old_value = doc['value']['old']
        new_value = doc['value']['new']
        old_date = doc['updated_pre']
        diff = new_value-old_value

        new_data = f'{new_date} - {old_value} ({old_date}) ==>> {new_value} ({diff})'
        print(new_data)
        # st.write(f"{new_date} ==>> {count} Articles")
        # print(f"{new_date} ==>> {count} Articles")
        # new_data = f"{new_date} ==>> {count} Articles"
        write_to_file(new_data)