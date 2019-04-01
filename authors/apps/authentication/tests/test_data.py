no_login_credentialds_data = {}

login_credentials_data =  {
            "user": {
                "username": "user",
                "email": "testuser@gmail.com",
                "password": "user@12345"
            }
        }
test_user_data =  {
            "user": {
                "username": "testuser",
                "email": "testuser2@gmail.com",
                "password": "user@12345"
            }
        }
test_user_data_password_change =  {
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
                 "email":"testuser@gmail.com",
    			 "password":"user@12345"
         }
        }

auth_change_password = {
    "user": {
                 "email":"testuser@gmail.com",
    			 "password":"abcdefgh"
         }
}

invalid_login_data = {
           "user": {
                 "email":"testuser@gmail.comhhfhf",
    			 "password":"user@12345"
         }
        }
login_data_miss_email = {
                "user": {           
                    "password":"kiryowa1993"
                }
        }
login_data_miss_password = {
                "user": {           
                    "email":"franciskiryowa68@gmail.com"
                }
        }
      
empty_login_data_object = {}
