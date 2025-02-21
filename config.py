import os
import pymysql
class Config:
    DB_HOST = os.getenv("DB_HOST", "mysql-1ce5eb8-jose-eae6.e.aivencloud.com")
    DB_USER = os.getenv("DB_USER", "avnadmin")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "AVNS_u4xv4qhGhPxOY13Gm-L")
    DB_NAME = os.getenv("DB_NAME", "globant_challenge")
    DB_PORT = int(os.getenv("DB_PORT", 20906))  
    DB_CHARSET = os.getenv("DB_CHARSET", "utf8mb4") 
    DB_CURSORCLASS = "DictCursor"

