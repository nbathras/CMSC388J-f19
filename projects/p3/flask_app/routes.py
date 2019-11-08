from flask_app import app, db
from flask import render_template, request, redirect, url_for
from flask_app.models import *

from flask_app.forms import *

import datetime

@app.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.all()
    form = PostForm()
    default_date_time = datetime.date.today().strftime('%B %d, %Y')

    new_posts = list()
    for post in posts:
        new_post = dict()
        new_post["user_name"] = post.user.name
        new_post["date"]      = post.date
        new_post["title"]     = post.title
        new_post["user_id"]   = post.user.id
        new_post["id"]        = post.id

        if len(post.content) < 250:
            new_post["content"] = post.content
        else:
            new_post["content"] = post.content[:250] + "..."

        new_posts.append(new_post)
    posts = new_posts

    if request.method == 'POST':
        if form.validate():
            print("form is valid")
            user = User.query.filter_by(email=form.email.data).first()
            
            if user is None:
                print("Create new User + Post")
                user = User(
                    name  = form.author.data, 
                    email = form.email.data
                )
                # in order to access user.id in the next initialization you must add
                #   and commit the new object to the session
                db.session.add(user)
                db.session.commit()
            
            post = Post(
                author_id = user.id,
                user      = user,
                title     = form.title.data, 
                content   = form.content.data,
                date      = form.date.data,
            )
            db.session.add(post)
            db.session.commit()

        else:
            print("form is invalid")

        return redirect('/')

    return render_template(
        'index.html', 
        posts             = posts, 
        form              = form, 
        default_date_time = default_date_time
    )

@app.route('/<name>_<int:user_id>', methods=['GET'])
def profile(name, user_id):
    posts           = Post.query.filter_by(author_id=int(user_id))
    number_of_posts = posts.count()
    user            = User.query.get(int(user_id))

    new_posts = list()
    for post in posts:
        new_post = dict()
        new_post["user_name"] = post.user.name
        new_post["date"]      = post.date
        new_post["title"]     = post.title
        new_post["user_id"]   = post.user.id
        new_post["id"]        = post.id

        if len(post.content) < 250:
            new_post["content"] = post.content
        else:
            new_post["content"] = post.content[:250] + "..."

        new_posts.append(new_post)
    posts = new_posts

    return render_template('user.html', posts=posts, user=user, number_of_posts=number_of_posts)

@app.route('/post_detail/<post_title>_<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_title, post_id):
    post              = Post.query.get(int(post_id))
    comments          = Comment.query.filter_by(post_id=int(post_id))
    form              = CommentForm()
    default_date_time = datetime.date.today().strftime('%B %d, %Y')

    # show that the __repr__ works for each of the objects
    print(str(post))
    print("")
    print(str(post.user))
    print("")
    for comment in comments:
        print(comment)
        print("")

    if request.method == 'POST':
        if form.validate():
            print("form is valid")

            comment = Comment(
                post    = post,
                author  = form.author.data,
                content = form.content.data,
                date    = form.date.data
            )

            db.session.add(comment)
            db.session.commit()
        else:
            print("form is invalid")

        return redirect('/post_detail/' + str(post_title) + '_' + str(post_id))

    return render_template(
        'post.html', 
        post              = post, 
        comments          = comments,
        form              = form, 
        default_date_time = default_date_time
    )
