from peewee import *
from user_srv.config import config


class BaseModel(Model):
    class Meta:
        database = config.DB


GENDER_CHOICE = (
    (1, '女'),
    (2, '男')
)

ROLE_CHOICE = (
    (1, '普通用户'),
    (2, '管理员')
)


class User(BaseModel):
    mobile = CharField(max_length=11, index=True, unique=True, verbose_name='手机号码')
    password = CharField(max_length=100, verbose_name='密码')
    nick_name = CharField(max_length=20, verbose_name='昵称')
    head_url = CharField(max_length=200, verbose_name='头像')
    birthday = DateField(null=True, verbose_name='生日')
    address = CharField(max_length=200, null=True, verbose_name='地址')
    desc = TextField(null=True, verbose_name='个人简介')
    gender = IntegerField(choices=GENDER_CHOICE, null=True, verbose_name='性别')
    role = IntegerField(default=1, choices=ROLE_CHOICE, verbose_name='角色')


if __name__ == '__main__':
    config.DB.create_tables([User])
