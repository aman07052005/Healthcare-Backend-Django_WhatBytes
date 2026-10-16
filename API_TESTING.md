# Postman quick test

1. Register with `POST http://127.0.0.1:8000/api/auth/register/`.
2. Login with `POST http://127.0.0.1:8000/api/auth/login/`; copy `access`.
3. For all subsequent requests, set Authorization type to Bearer Token and paste the access token.
4. Create a patient, create a doctor, then create a mapping using their numeric IDs.
5. Test unauthorized access by removing the Authorization header (expected 401).
6. Test ownership by logging in as a second user and attempting to read the first user's patient (expected 404).
