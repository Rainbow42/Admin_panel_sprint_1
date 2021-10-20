import os

DSL = {
    'dbname': os.getenv('DB_NAME', 'postgres'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('PASSWORD', 'password'),
    'host': os.getenv('HOST', '127.0.0.1'),
    'port': os.getenv('PORT', 5432)
}
