import hashlib

# For demonstration purposes, user credentials are hardcoded.
# In a production environment, replace this with a secure database connection.
USER_CREDENTIALS = {"admin": hashlib.sha256("password123".encode()).hexdigest()}

def verify_login(username, password):
    """
    Verifies the provided username and password against stored credentials

    Note:
    This function currently uses hardcoded credentials for demonstration purposes
    In a real-world scenario, you should fetch the hashed password from a secure database 
    and compare it with the hashed version of the provided password

    Args:
        username (str): The username provided by the user
        password (str): The password provided by the user
    
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return USER_CREDENTIALS.get(username) == hashed_password
