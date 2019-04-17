article_data = {
        "title":"Post about our TTl",
        "description":"He is good at what he does",
        "body":"This is a post describing everything we did in sims one",
        "tags": ["sports", "Arsenal"]
}


register_user1_data =  {
            "user": {
                "username": "maria22",
                "email": "maria@gmail.com",
                "password": "Maria@12345"
            }
}

register_user2_data =  {
            "user": {
                "username": "joan22",
                "email": "joan@gmail.com",
                "password": "Joan@12345"
            }
}

update_user_profile_data1 = {
    "firstname": "Maria",
    "lastname": "Nakalungi",
    "bio": "I love travelling",
    "image": "https://www.django-rest-framework.org/api-guide/maria.png"
}

comment_data = {
  "comment": {
    "body": "We love our TTl",
  }
}

highlight_comment_data = {
  "comment": {
    "body": "We love our TTl",
    "start_position":1,
	  "end_position":4
  }
}

out_of_range_data = {
  "comment": {
    "body": "We love our TTl",
    "start_position":10,
	  "end_position":1000
  }
}

startpoint_less_endpoint = {
  "comment": {
    "body": "We love our TTl",
    "start_position":1000,
	  "end_position":10
  }
}

invalid_comment = {
  "comment": {
    "body": "We love our TTl",
    "start_position":"1",
	  "end_position":4
  }
}

comment_data1 = {
  "comment": {
    "body": "We love working as a team"
  }
}

reply_to_comment1 =  {
  "comment": {
    "body": "He replies to slack texts instantly"
  }
}

reply_to_comment2 =  {
  "comment": {
    "body": "He makes coding fun"
}
}   

update_comment_data = {
  "comment": {
    "body": "Updated by Francis"
  }
}
