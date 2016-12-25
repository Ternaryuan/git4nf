import os, warnings
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 秘钥用于实现CSRF保护,为了安全应定义在环境变量中
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_simple_key'
    # 追踪对象的修改并且发送信号(不是很懂)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # TODO: delete this line?
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 定义邮件名的前缀
    APP_MAIL_SUBJECT_PREFIX = '[NewFolder]'
    # 定义发件人信息
    warnings.warn('上线前将发件人邮箱改为实际使用的邮箱!')
    APP_MAIL_SENDER = 'NewFolder Admin <993873600@qq.com>'
    # 定义管理员
    APP_ADMIN = os.environ.get('NF_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # 开启调试模式
    DEBUG = True
    # 使用谷歌SMTP服务器
    MAIL_SERVER = 'smtp.qq.com'
    # 使用587端口发送邮件
    MAIL_PORT = 25
    # 使用TLS(安全传输层协议)保护数据
    MAIL_USE_TLS = True
    # 定义邮箱用户名和密码,从环境变量中读取
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # TODO: delete this!
    MAIL_USERNAME = '993873600@qq.com'
    MAIL_PASSWORD = 'Asdfghjkl1'
    # 定义调试使用的数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    # 开启测试
    TESTING = True
    # 定义测试使用的数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class ProductionConfig(Config):
    # 定义生产环境下使用的数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
