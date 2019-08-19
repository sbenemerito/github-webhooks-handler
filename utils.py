import os
import hashlib
import hmac


def verify_signature(data, signature):
    """
    Generate a hash signature using the `SECRET_TOKEN` (taken from environment
    variables) and the payload body. Return a `boolean` value which tells if
    the generated signature and GitHub's signature match.

    Validating payloads: https://developer.github.com/webhooks/securing/
    """
    secret_token = bytes(os.environ.get('SECRET_TOKEN'), 'utf-8')
    auth_code = hmac.new(secret_token, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + auth_code.hexdigest(), signature)
