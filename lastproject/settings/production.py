from .base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['movie-aim.yarufnjmpv.ap-northeast-2.elasticbeanstalk.com']