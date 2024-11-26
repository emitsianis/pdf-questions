import os

import redis
from dotenv import load_dotenv

load_dotenv()

client = redis.Redis.from_url(
    os.environ["REDIS_URI"],
    decode_responses=True,
)
