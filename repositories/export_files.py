import os

from core.config import init_redis_pool

path = os.getcwd()
filename = 'quiz_result.csv'
file_path = os.path.join(path, filename)


def get_csv_from_redis(key: str):
    connect = init_redis_pool()
    with open(file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(connect.get(key).decode('utf-8'))
    return new_file


def get_all_csv_file_redis(key: str):
    connect = init_redis_pool()
    with open(file_path, 'w', encoding='utf-8') as new_file:
        for keys in connect.scan_iter(key):
            new_file.writelines(f"{keys.decode('utf-8').split('-')[-1]} - {connect.get(keys).decode('utf-8')}\n")
    return new_file
