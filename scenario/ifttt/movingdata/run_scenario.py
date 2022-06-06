import shutil
import redis


def move_file(
    src_path: str,
    des_path: str
):
    """Moves a file from the source a destination."""
    shutil.copy(src_path, des_path)


if __name__ == '__main__':
    redis_client = redis.Redis('localhost', 6379)
    src = '../../../data/move_src_data'
    des = '../../../data/move_des_data'

    move_file(src, des)
    redis_client.set('moved', 1)
