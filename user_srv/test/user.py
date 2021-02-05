import grpc
from user_srv.proto import user_pb2_grpc, user_pb2


class UserTest:
    def __init__(self):
        channel = grpc.insecure_channel('127.0.0.1:50051')
        self.stub = user_pb2_grpc.UserStub(channel)

    def user_list(self):
        resp: user_pb2.UserListResponse = self.stub.GetUserList(user_pb2.PageInfoRequest(page=2, size=2))
        for u in resp.data:
            print(u.mobile, u.id)

    def get_user_by_id(self, id):
        u: user_pb2.UserInfoResponse = self.stub.GetUserById(user_pb2.IdRequest(id=id))
        print(u.mobile)

    def add_user(self, nickName, mobile, password):
        return self.stub.CreateUser(user_pb2.CreateUserRequest(
            nickName=nickName,
            mobile=mobile,
            password=password))


if __name__ == '__main__':
    test = UserTest()
    # test.user_list()
    # test.get_user_by_id(3)
    test.add_user(nickName='Scott.She', mobile='18702195000', password='123456')
