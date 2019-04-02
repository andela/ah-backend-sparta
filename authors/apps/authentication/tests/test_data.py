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


# Social Data
invalid_facebook_token = {
    'user_token' : {
        'auth_token': 'rxdtcfyvgubhinjihiguftyrdyfugih'
    }
}

invalid_google_token = {
    'user_token' : {
        'auth_token': 'EAAFV9Sn6cKIBAJvKphYGHJ8hiYmzRhxFVLTugGtmpwVJEQB8xiNR7mpEZAWQcoHgTSMNJLRV9dE9g0b3vFX4A06pTrqg66cg1pRMNzfzWJhCHzVZBreUmnwXR7aoPHEJugA8ttZCS1baWvC932umvcuWJ8UBQiLBHZBAIOH8ZBSNZBUGB6mH7dOhZAn6qjhZBwWkPWSbTDSUgwZDZD'
    }
}

invalid_twitter_tokens = {
    'user_token' : {
        'auth_token': 'hksjnd_@ksljdGHJ8hiYmzRhxFVLTugGtmpwVJEQB8xiNR7mpEZAW QcoHgTSMNJLRV9dE9g0b3vFX4A06pTrqg66cg1pRMNzfzWJhCHzVZBreUmnwXR7aoPHEJugA8ttZCS1baWvC932umvcuWJ8UBQiLBHZBAIOH8ZBSNZBUGB6mH7dOhZAn6qjhZBwWkPWSbTDSUgwZDZD'
    }
}

one_twitter_token = {
    'user_token' : {
        'auth_token': 'hksjnd_@ksljdGHJ8hiYmzRhxFVLTugGtmpwVJEQB8xiNR7mpEQcoHgTSMNJLRV9dE9g0b3vFX4A06pTrqg66cg1pRMNzfzWJhCHzVZBreUmnwXR7aoPHEJugA8ttZCS1baWvC932umvcuWJ8UBQiLBHZBAIOH8ZBSNZBUGB6mH7dOhZAn6qjhZBwWkPWSbTDSUgwZDZD'
    }
}

social_reg_no_email_data = {
    'email': '',
    'username': 'testname'
}

social_reg_data = {
    'email': 'test@testmail.com',
    'username': 'testname'
}
