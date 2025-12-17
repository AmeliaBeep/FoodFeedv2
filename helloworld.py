from flask import Flask

app = Flask(__name__)

def show_user(username):
    # Greet the user
    return f'Hello {username} !'
  
app.add_url_rule('/user/<username>', 'show_user', show_user)

if __name__ == "__main__":
    app.run(debug=True)