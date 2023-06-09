from pydantic import BaseSettings
import cloudinary


class Settings(BaseSettings):
    sqlalchemy_database_url: str = 'postgresql+psycopg2://user:password@localhost:5466/postgres'
    secret_key: str = 'secret_key'
    algorithm: str = 'HS256'
    # mail_username: str = 'example@meta.ua'
    # mail_password: str = 'password'
    # mail_from: str = 'example@meta.ua'
    # mail_port: int = 465
    # mail_server: str = 'smtp.meta.ua'
    redis_host: str = 'localhost'
    redis_port: int = 6366

    cloudinary_name: str = 'name'
    cloudinary_api_key: int = 991546536478543
    cloudinary_api_secret: str = 'secret'

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


def cloudinary_config():
    """
    The cloudinary_config function is used to configure the cloudinary library with your Cloudinary account's details.
    This function should be called before using any of the other cloudinary functions.

    :return: The cloudinary configuration
    """
    cloudinary.config(
             cloud_name=settings.cloudinary_name,
             api_key=settings.cloudinary_api_key,
             api_secret=settings.cloudinary_api_secret,
             secure=True
         )

