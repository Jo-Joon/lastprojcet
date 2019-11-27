from .base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY', default='l*5tk=#79t(cam%@30l4eox4k&^9uv--p6_40-1v6ahov=x#sa')

DEBUG = True

ALLOWED_HOSTS = []