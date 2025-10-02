import secrets

def generate_token():
    return secrets.token_urlsafe(32)


if __name__ == '__main__':
    generate_token()
