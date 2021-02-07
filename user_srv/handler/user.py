import grpc
import time
from datetime import date
from loguru import logger
from passlib.hash import pbkdf2_sha256

from user_srv.proto import user_pb2, user_pb2_grpc
from user_srv.model.models import User
from peewee import DoesNotExist
from google.protobuf import empty_pb2


def convert_user_to_resp(user):
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

    if user.head_url:
        user_resp.headUrl = user.head_url

    if user.address:
        user_resp.address = user.address

    if user.desc:
        user_resp.desc = user.desc

    return user_resp


class UserServicer(user_pb2_grpc.UserServicer):

    @logger.catch
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
            u = convert_user_to_resp(user)
            rsp.data.append(u)
        return rsp

    @logger.catch
    def GetUserById(self, request: user_pb2.IdRequest, context):
        # 数据库操作都有可能会出现异常， 所以要捕获
        try:
            user = User.get(User.id == request.id)
            return convert_user_to_resp(user)
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('用户不存在')
            return user_pb2.UserInfoResponse()

    @logger.catch
    def GetUserByMobile(self, request: user_pb2.MobileRequest, context):
        # 数据库操作都有可能会出现异常， 所以要捕获
        try:
            user = User.get(User.mobile == request.mobile)
            return convert_user_to_resp(user)
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('用户不存在')
            return user_pb2.UserInfoResponse()

    @logger.catch
    def CreateUser(self, request: user_pb2.CreateUserRequest, context):
        # 数据库操作都有可能会出现异常， 所以要捕获
        try:
            User.get(User.mobile == request.mobile)
            # 利用context会直接就报错
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('用户已存在')

            return user_pb2.UserInfoResponse()
        except DoesNotExist:
            pass

        user = User()
        user.nick_name = request.nickName
        user.mobile = request.mobile
        user.password = pbkdf2_sha256.hash(request.password)
        user.save()

        return convert_user_to_resp(user)

    @logger.catch
    def UpdateUser(self, request: user_pb2.UpdateUserRequest, context):
        # 数据库操作都有可能会出现异常， 所以要捕获
        try:
            user = User.get(User.id == request.id)
            if request.nickName:
                user.nick_name = request.nickName

            if request.gender:
                user.gender = request.gender

            if request.role:
                user.role = request.role

            if request.headUrl:
                user.head_url = request.headUrl

            if request.address:
                user.address = request.address

            if user.desc:
                user.desc = request.desc

            if request.birthday:
                user.birthday = date.fromtimestamp(request.birthday)
            user.save()
            return empty_pb2.Empty()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('用户不存在')
            return user_pb2.UserInfoResponse()
