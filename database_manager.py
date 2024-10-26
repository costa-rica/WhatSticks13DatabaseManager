import sqlalchemy
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from common.config_and_logger import config, logger_db_manager
import shutil
import os
from ws_models import engine, sessionmaker , DatabaseSession, text, Users
import bcrypt

salt = bcrypt.gensalt()
new_engine_str = f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_SERVER}/{config.MYSQL_DATABASE_NAME}"
new_engine = create_engine(new_engine_str)

def drop_and_create_database(engine, database_name):
    logger_db_manager.info(f'- in drop_and_create_database -')
    logger_db_manager.info(f"database_name: {database_name}")
    with engine.connect() as connection:
        try:
            connection.execute(text(f"DROP DATABASE IF EXISTS {database_name};"))
            connection.execute(text(f"CREATE DATABASE {database_name};"))
            logger_db_manager.info(f"Database {database_name} dropped and recreated successfully.")
        except SQLAlchemyError as e:
            logger_db_manager.info(f"An error occurred: {e}")

def delete_helper_files():
    logger_db_manager.info(f'- in delete_database_helper, ios_helper, and user_files -')
    if os.path.exists(config.DATABASE_HELPER_FILES):
        shutil.rmtree(config.DATABASE_HELPER_FILES)
    if os.path.exists(config.WS_IOS_HELPER_FILES):
        shutil.rmtree(config.WS_IOS_HELPER_FILES)
    if os.path.exists(config.USER_FILES):
        shutil.rmtree(config.USER_FILES)


def create_tables( ):
    logger_db_manager.info(f'- in create_tables -')
    Base.metadata.create_all(new_engine)
    logger_db_manager.info("Tables created successfully.")


def create_admin_user():
    logger_db_manager.info(f'- in create_admin_user -')
    DatabaseSession = sessionmaker(bind=new_engine)
    db_session = DatabaseSession()
    hash_pw = bcrypt.hashpw(config.ADMIN_PASSWORD.encode(), salt)
    new_user = Users(
        email = config.ADMIN_EMAIL, 
        password = hash_pw, timezone = "Etc/GMT",
        admin_permission=True
        )
    db_session.add(new_user)
    db_session.commit()
    logger_db_manager.info(f'- created admin user: {config.ADMIN_EMAIL} -')

if __name__ == "__main__":
    logger_db_manager.info(f'--- Started What Sticks 13 Database Manager ---')
    drop_and_create_database(engine, config.MYSQL_DATABASE_NAME)
    delete_helper_files()
    create_tables()
    create_admin_user()
