import grpc
import os
import sys
import signal
import argparse
from concurrent import futures
from loguru import logger

# 通过server运行需要知道项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, BASE_DIR)

from user_srv.proto import user_pb2_grpc
from user_srv.handler.user import UserServicer


def on_exit(sign, frame):
    logger.info("程序退出")
    sys.exit(0)


def serve():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',
                        nargs='?',
                        type=str,
                        default='127.0.0.1',
                        help='binding ip'
                        )

    parser.add_argument('--port',
                        nargs='?',
                        type=int,
                        default=50051,
                        help='the listening port'
                        )

    args = parser.parse_args()

    logger.add("logs/user_srv_{time}.log")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    server.add_insecure_port(f'{args.ip}:{args.port}')
    logger.info(f'启动服务：{args.ip}:{args.port}')

    # 主进程退出信号监听, 暂时监听两种信号
    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)

    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
