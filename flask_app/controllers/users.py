from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def index():
    users = User.get_all()
    print(users)
    return render_template("index.html", all_users=users)


@app.route('/users/new', methods=['GET'])
def new_page():
    return render_template("create_page.html")

@app.route("/create/users", methods=["POST"])
def create():
    # check if the form into is valid is input
    if User.is_valid_user(request.form):
        User.save(request.form)
        return redirect('/')
    # create the user if valid
    # if not -- send direct the user back to the create page
    else:
    # to be able show the message
        return redirect('/users/new')

@app.route("/users/edit/<int:id>")
def edit(id):
    data = {
        "id":id
    }
    return render_template("create_page.html", users=User.get_one(data))


@app.route("/users/update",methods=['POST'])
def update():
    User.update(request.form)

    return redirect("/")

@app.route("/user/show/<int:id>")
def show(id):
    data = {
        "id":id
    }
    return render_template("show.html", users=User.get_one(data))

@app.route('/user/destroy/<int:id>')
# "/user/destroy/{{ users.id }}"
def destroy(id):
    data = {
        'id':id
    }
    User.destroy(data)
    return redirect('/')





