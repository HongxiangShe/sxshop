import grpc

from user_srv.proto import user_pb2, user_pb2_grpc
from user_srv.model.models import User
# from user_srv.proto.user_pb2 import UserInfoResponse


class UserServicer(user_pb2_grpc.UserServicer):
    def GetUserList(self, request: user_pb2.PageInfoRequest, context):

        rsp = user_pb2.UserListResponse()

        users = User.select()
        for user in users:
            userInfoRes = user_pb2.UserInfoResponse()
            userInfoRes.id = user.id
            userInfoRes.password = user.password
            userInfoRes.mobile = user.mobile
            userInfoRes.role = user.role

            if user.nick_name:
                userInfoRes.nickName = user.nick_name

            if user.gender:
                userInfoRes.gender = user.gender

            if user.birthday:
                userInfoRes.birthDay

            rsp.data.append(userInfoRes)