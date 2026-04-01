from pymongo import MongoClient

def connect_to_mongo():
    client = MongoClient('mongodb://admin:q8vm5dz-h29piX%3FMo%26%3ClO4e0zn@192.168.11.10:27017/?authSource=admin&maxPoolSize=10&minPoolSize=0&maxIdleTimeMS=50000&directConnection=true')
    return client["zeno_db"]

def write_to_file(new_data):
    file_name = f'timelogs.txt'
    with open(file_name, "a") as file:
        file.write(f'{new_data}\n')

def connect_to_data():
    client = MongoClient('mongodb+srv://jonpuray:vYk9PVyQ7mQCn0Rj@cluster1.v4m9pq1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1')
    db = client['autoupload']
    collection = db['data']
    return collection