
import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

def is_valid_email(email):
    return re.match(EMAIL_REGEX, email) is not None
