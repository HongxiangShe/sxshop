import time

from user_srv.proto import user_pb2, user_pb2_grpc
from user_srv.model.models import User


class UserServicer(user_pb2_grpc.UserServicer):
    def GetUserList(self, request: user_pb2.PageInfoRequest, context):

        start = 0
        page_size = 20

        if request.size & request.size > 0:
            page_size = request.size

        if request.page:
            page = max(1, request.page)
            start = page_size * (page - 1)

        users = User.select()
        users = users.limit(page_size).offset(start)
        rsp: user_pb2.UserListResponse = user_pb2.UserListResponse()
        for user in users:
            user_resp = user_pb2.UserInfoResponse()
            user_resp.id = user.id
            user_resp.password = user.password
            user_resp.mobile = user.mobile
            user_resp.role = user.role

            if user.nick_name:
                user_resp.nickName = user.nick_name

            if user.gender:
                user_resp.gender = user.gender

            if user.birthday:
                user_resp.birthday = int(time.mktime(user.birthday.timetuple()))

            rsp.data.append(user_resp)
        return rsp
