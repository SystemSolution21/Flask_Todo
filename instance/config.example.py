# instance/config.py
SECRET_KEY = """
'secret-key-that-you-should-change'
Generate a random secret key
```pwsh
python -c "import secrets; print(secrets.token_hex(24))"
```
"""
SQLALCHEMY_DATABASE_URI = (
    "postgresql://your_db_user:your_db_password@localhost/your_db_name"
)
