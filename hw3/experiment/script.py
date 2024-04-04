import json
import redis
import time


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def save_and_read_from_redis(data, redis_client):
    start_time = time.time()
    redis_client.set('json_string', json.dumps(data))
    print(f"save: string: {time.time() - start_time:.5f} seconds")

    start_time = time.time()
    redis_client.get('json_string')
    print(f"read: string: {time.time() - start_time:.5f} seconds")

    if isinstance(data, list) and data:
        start_time = time.time()
        for key, value in data[0].items():
            redis_client.hset('json_hash', key, json.dumps(value))
        print(f"save: hash: {time.time() - start_time:.5f} seconds")

        start_time = time.time()
        for key in data[0].keys():
            redis_client.hget('json_hash', key)
        print(f"read: hash: {time.time() - start_time:.5f} seconds")

    start_time = time.time()
    for item in data:
        redis_client.rpush('json_list', json.dumps(item))
    print(f"save: list: {time.time() - start_time:.5f} seconds")

    start_time = time.time()
    redis_client.lrange('json_list', 0, -1)
    print(f"read: list: {time.time() - start_time:.5f} seconds")

    start_time = time.time()
    for index, item in enumerate(data):
        redis_client.zadd('json_zset', {json.dumps(item): index})
    print(f"save: zset: {time.time() - start_time:.5f} seconds")

    start_time = time.time()
    redis_client.zrange('json_zset', 0, -1)
    print(f"read: zset: {time.time() - start_time:.5f} seconds")


if __name__ == "__main__":
    json_file_path = 'big.json'
    json_data = read_json_file(json_file_path)

    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    save_and_read_from_redis(json_data, redis_client)
