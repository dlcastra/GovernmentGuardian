# Required secret keys
```
AUTH0_CLIENT_ID
AUTH0_CLIENT_SECRET
AUTH0_DOMAIN
DEFAULT_FROM_EMAIL
EMAIL_SECRET_KEY
```

### Required commands
1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Apply migration:
    ```
    python manage.py migrate
    ```