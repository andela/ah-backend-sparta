no_login_credentialds_data = {
    "user": {
        
    }
}

login_credentials_data = {
    "user": {
        "username": "user",
        "email": "testuser@gmail.com",
        "password": "User@12345"
    }
}
login_same_username_different_email = {
     "user": {
        "username": "user",
        "email": "testuser2@gmail.com",
        "password": "User@12345"
    }
}

test_user_data = {
    "user": {
        "username": "testuser",
        "email": "testuser2@gmail.com",
        "password": "User@12345"
    }
}
test_user_data_password_change = {
    "user": {
        "username": "testuser",
        "email": "testuser2@gmail.com",
        "password": "abcdefgh"
    }
}
empty_string_username = {
    "user": {
        "username": "",
        "email": "userstest67@gmail.com",
        "password": "Users@12345"
    }
}
empty_string_email = {
    "user": {
        "username": "kiryowa22",
        "email": "",
        "password": "users@134"
    }
}
empty_string_password = {
    "user": {
        "username": "kiryowa22",
        "email": "kiryowa@gmail.com",
        "password": ""
    }
}
invalid_email_data = {
    "user": {
        "username": "Rogha1996",
        "email": "Rogha",
        "password": "12345678"
    }
}
login_data = {
    "user": {
        "email": "testuser@gmail.com",
        "password": "User@12345"
    }
}

auth_change_password = {
    "user": {
        "email": "testuser@gmail.com",
        "password": "abcdefgh"
    }
}

invalid_login_data = {
    "user": {
        "email": "testuser@gmail.comhhfhf",
        "password": "user@12345"
    }
}
login_data_miss_email = {
    "user": {
        "password": "kiryowa1993"
    }
}
login_data_miss_password = {
    "user": {
        "email": "franciskiryowa68@gmail.com"
    }
}

empty_login_data_object = {}

# Registration data
invalid_registration_data = {
    "user": {
        "username": "kani",
        "email": "kani@gmail.com"
    }
}

username_containing_spaces = {
	 "user": {
        "username": "jose      ph123",
        "email": "jack@gmail.com",
        "password":"Joseph@12345"
  }
}
password_containing_spaces = {
	 "user": {
        "username": "joseph123",
        "email": "jack@gmail.com",
        "password":"Joseph    @12345"
  }
}

password_containing_spaces = {
	 "user": {
        "username": "joseph123",
        "email": "jack@gmail.com",
        "password":"Joseph     @12345"
  }
}

username_and_password_not_provided = {
	 "user": {
        "password":"joseph@1234"
    }
}
