from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db,User,Feedback
from forms import RegForm, LoginForm, FeedbackForm, DeleteForm
from sqlalchemy.exc import IntegrityError




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug= True
toolbar = DebugToolbarExtension(app)






app.app_context().push()


connect_db(app)

@app.route('/')
def redirect_to_reg():
    return redirect('/register')

@app.route('/register', methods=['GET'])
def register_user():
    form=RegForm()
    return render_template("register.html", form=form)

@app.route('/register', methods=['POST'])
def regform_handler():
    form=RegForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username,password,email,first_name,last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("Username taken. Please pick another username.")
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!',"success")
        return redirect('/users/<username>')
    return render_template("register.html", form=form, username=username,password=password,
                           email=email,first_name=first_name,last_name=last_name)

##NEED TO FIGURE OUT HOW TO FILTER DOWN RESULTS TO CURRENT USER ONLY
@app.route('/users/<username>')
def show_user_details(username):
    if "username" not in session:
        flash("Please login first!","danger")
        return redirect('/login')
    
    
    user= User.query.get(username)
    form = DeleteForm()
 
    return render_template("secret.html", user=user, form=form)


@app.route('/login')
def show_login_form():
    form=LoginForm()
    return render_template("login.html", form=form)

@app.route('/login', methods=['POST'])
def handle_login_form():
    form=LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user =User.authenticate(username,password)
        if user:
            flash(f"Welcome Back!,{user.username}!", "success")
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ['Invalid username/ password'] 

    return render_template('login.html', form=form)

@app.route("/logout")
def logout():  
    session.pop("username")
    flash("Goodbye!","info")
    return redirect("/")

#WORK ON FIGUREING OUT HOW TO SEPARATE THIS ROUTE INTO GET and POST

@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show add-feedback form and process it."""

    if "username" not in session or username != session["username"]:         
        flash("Please login first!","danger")
        return redirect('/login')

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback.html", form=form)
    

##REVIEW THIS: WORK ON SEPARATING GET AND POST ROUTES
    
@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:         
        flash("Please login first!","danger")
        return redirect('/login')

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("feedbackedit.html", form=form, feedback=feedback)


#REVIEW THIS
@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        flash("Please login first!","danger")
        return redirect('/login')


    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")

#REVIEW

@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user and redirect to login."""

    if "username" not in session or username != session['username']:
        flash("Please login first!","danger")

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")













# if "username" not in session or username != session["username"]:         
    #     flash("Please login first!","danger")
    #     return redirect('/login')





# @app.route("/users/{username}/feedback/new", methods=["GET", "POST"])
# def new_feedback(username):
#     """Show add-feedback form and process it."""

#     if "username" not in session:         
#         flash("Please login first!","danger")
#         return redirect('/login')

#     form = FeedbackForm()

#     if form.validate_on_submit():
#         title = form.title.data
#         content = form.content.data

#         feedback = Feedback(
#             title=title,
#             content=content,
#             username=username
#         )

#         db.session.add(feedback)
#         db.session.commit()

#         return redirect(f"/users/{feedback.username}")

#     else:
#         return render_template("feedback.html", form=form)
    








































