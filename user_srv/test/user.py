import grpc
from user_srv.proto import user_pb2_grpc, user_pb2


class UserTest:
    def __init__(self):
        channel = grpc.insecure_channel('127.0.0.1:50051')
        self.stub = user_pb2_grpc.UserStub(channel)

    def user_list(self):
        resp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfoRequest(page=1, size=5))
        for u in resp.data:
            print(u.mobile, u.id)


if __name__ == '__main__':
    user = UserTest()
    user.user_list()
