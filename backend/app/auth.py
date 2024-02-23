import pyrebase

config = {
    'apiKey': "AIzaSyB7OO9bedMLka553ftTdg9TKi0fG5Kxdbo",
    'authDomain': "authenticatepy-3b4eb.firebaseapp.com",
    'projectId': "authenticatepy-3b4eb",
    'storageBucket': "authenticatepy-3b4eb.appspot.com",
    'messagingSenderId': "61269466253",
    'appId': "1:61269466253:web:f4ca52255bf027133196c4",
    'measurementId': "G-9ZWP2R8LHV",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# EXAMPLES FOR LATER USE:
# user = auth.create_user_with_email_and_password(email, password)
# user = auth.sign_in_with_email_and_password(email, password)
# info = auth.get_account_info(user['idToken'])
# auth.send_email_verification(user['idToken'])
# auth.send_password_reset_email(email)