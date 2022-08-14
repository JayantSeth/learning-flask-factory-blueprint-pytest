# Learning Flask Blueprint Factory Pytest

I have learned following concept in this app:
1. Blueprint
2. Application Factory
3. Testing: pytest

Minor stuffs:
   1. Loading config from python file and object.

I have practiced following two skills:
1. JWT Based Authentication.
2. One to Many Association

Blueprint for following resource:
1. Auth
2. Author-Title

Tables:
Users: id, username, password, email

Author: id, name, age, titles

Title: id, title, summary, author_id


References:
```buildoutcfg
Getting configuration from file: https://hackersandslackers.com/configure-flask-applications/
Answer to Why blueprint is necessary with flask_restful: https://stackoverflow.com/questions/62200557/what-is-the-benefit-of-using-blueprint-in-flask-restful
Testing: https://testdriven.io/blog/flask-pytest/
Testing: https://stackoverflow.com/questions/45703591/how-to-send-post-data-to-flask-using-pytest-flask
Testing: https://pytest-flask.readthedocs.io/en/latest/tutorial.html
https://github.com/vimalloc/flask-jwt-extended/issues/308

```

To Install Dependencies:
```buildoutcfg
pip install -r requirements.txt
```

To run the application :
```buildoutcfg
flask --app application run
```


To run the tests :
```buildoutcfg
pytest --no-header -v
```