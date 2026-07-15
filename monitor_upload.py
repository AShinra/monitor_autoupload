from datetime import date, datetime, timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
from common import connect_to_data, connect_to_mongo, write_to_file

if __name__ == '__main__':

    # get collection from mongodb
    db = connect_to_mongo()
    collection = db["articles_app_article"]    

    # get date today
    _date = date.today()
    print(f'GENERATED: {datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}')

    write_to_file(f'\n*ONLINE AUTOMATED PICKUPS TRACKING*')
    write_to_file(f'GENERATED: {datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}')
    write_to_file(f'\n*DAILY SUMMARY*')

    data_collection = connect_to_data()
    last_doc = data_collection.find_one(sort=[("_id", -1)])
    header_date = last_doc["updated_at"]

    write_to_file(f'LAST UPDATE: {header_date}')
    print(f'LAST UPDATE: {header_date}')
    # generate dates from the range i
    for i in range (0, 6):
        new_date = _date - timedelta(days=i)
        _month= new_date.month
        _day= new_date.day
        _year = new_date.year

        # yesterday
        yes_date = _date - timedelta(days=i+1)
        yes_month = yes_date.month
        yes_day = yes_date.day
        yes_year = yes_date.year

        # generate query
        query = {
        "created_by_id": ObjectId("619f0998a834a290ce4ef787"),
        "media_source.media_source_type_flag": "web",
        "date_publish": {
            "$gte": datetime(yes_year, yes_month, yes_day, 16, 0, 0),
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
            old_date = doc['updated_at']

            # update the document
            data_collection.update_one(
                {'date':str(new_date)},
                {'$set':{
                    'value.old':old_value,
                    'value.new':count,
                    'updated_pre':old_date,
                    'updated_at':f'{datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}'
                }})
        else:
            old_value = 0
            old_date = ''
            data = {
                'date':str(new_date),
                'value':{'old':old_value,'new':count},
                'updated_pre':old_date,
                'updated_at':f'{datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}'
            }

            data_collection.insert_one(data)
        
        diff = count-old_value

        new_data = f'{new_date} - {old_value} ==>> {count} ({diff})'
        print(f'@ {new_data}')
        # st.write(f"{new_date} ==>> {count} Articles")
        # print(f"{new_date} ==>> {count} Articles")
        # new_data = f"{new_date} ==>> {count} Articles"
        write_to_file(f'@ {new_data}')