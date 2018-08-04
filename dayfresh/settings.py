import os

HOST_IP = '127.0.0.1'
HOST_PORT = '80'
DATABASE_IP = '127.0.0.1'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5a!qwnfyi-*rpcxio*k$og9$#jo0$utbb@%mm4v_^(0ziq0q0m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
# DEBUG = False
#
# ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'tinymce',
    'user',
    'address',
    'goods',
    'order',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'dayfresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dayfresh.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dayfresh',
        'HOST': DATABASE_IP,
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '545733',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT='/Users/fire/fastdfs/dayfresh/static/'

# session
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = DATABASE_IP
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 1
SESSION_REDIS_PASSWORD = ''
SESSION_REDIS_PREFIX = 'session'

# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # email后端
EMAIL_HOST = "smtp.163.com"  # 服务器
EMAIL_PORT = 25  # 一般情况下都为25
EMAIL_HOST_USER = "jzl1091889012@163.com"  # 账号
EMAIL_HOST_PASSWORD = "wuhen1998"  # 密码
EMAIL_FROM = "天天生鲜<jzl1091889012@163.com>"  # 邮箱来自
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_USE_TLS = True  # 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
DOMAIN = 'http://' + HOST_IP + ':' + HOST_PORT + '/user/activate'

LOGIN_URL = '/user/login'

# 用户模型类
AUTH_USER_MODEL = "user.User"

# tinymce
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 600,
    'height': 400,
}

# FastDFS设置,自定义存储的类
DEFAULT_FILE_STORAGE = 'utils.fdfs.storage_util.FDFSStorage'
# FastDFS设置-客户端配置文件
FDFS_CLIENT_CONF = 'utils/fdfs/client.conf'
# FastDFS设置-url
FDFS_URL = 'http://%s:9999/' % HOST_IP

# 缓存到redis中
CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "redis://" + DATABASE_IP + ":6379/2",
        "TIMEOUT": 60,
    }
}

# 连接redis的对象
from redis import StrictRedis

redis_conn = StrictRedis(host=DATABASE_IP, port=6379, db=3)

# 全文检索HAYSTACK
HAYSTACK_CONNECTIONS = {
    'default': {
        # 使用whoosh引擎
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        # 默认的：'ENGINE':'haystack.backends.whoosh_backend.WhooshEngine',
        # 索引文件路径
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}

# 当添加，修改，删除数据时，自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

APP_PRIVATE_KEY_PATH=os.path.join(BASE_DIR,'order/app_private_key.pem')
ALIPAY_PUBLIC_KEY_PATH=os.path.join(BASE_DIR,'order/alipay_public_key.pem')