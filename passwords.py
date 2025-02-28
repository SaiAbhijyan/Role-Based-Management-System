from werkzeug.security import generate_password_hash

# Example password to hash
password = 'hr123'  # Replace this with the actual password you'd like to use
password_hash = generate_password_hash(password)

print(password_hash)
