import json
import uuid

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def fetch_post_by_id(post_id):
    with open("blogposts.json", "r") as fileobj:
        blogposts = json.load(fileobj)

    for post in blogposts:
        if post["id"] == post_id:
            index_of_post = blogposts.index(post)
        else:
            continue

    post = blogposts[index_of_post]
    return post, index_of_post


@app.route('/')
def index():
    # Fetch the blog posts from a file
    try:
        with open("blogposts.json", "r") as fileobj:
            blogposts = json.load(fileobj)
    except FileNotFoundError:
        blogposts = []

    return render_template("index.html", data=blogposts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        try:
            with open("blogposts.json", "r") as fileobj:
                blogposts = json.load(fileobj)
        except FileNotFoundError:
            blogposts = []

        next_uuid = str(uuid.uuid4())
        next_number = len(blogposts) + 1

        # Create a new blog post and add it to the list
        new_post = {
            "id": next_number,
            "uuid": next_uuid,
            "author": author,
            "title": title,
            "content": content
        }

        blogposts.append(new_post)

        with open("blogposts.json", "w") as fileobj:
            json.dump(blogposts, fileobj, indent=4)

        # Redirect to the home page
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    # Find the blog post with the given id and remove it from the list
    # Redirect back to the home page

    with open("blogposts.json", "r") as fileobj:
        blogposts = json.load(fileobj)

    for post in blogposts:
        if post["id"] == post_id:
            index_to_pop = blogposts.index(post)
        else:
            continue

    post, index = fetch_post_by_id(post_id)
    del blogposts[index]

    print(f"Deleted Blog Post: \n{post}")

    with open("blogposts.json", "w") as fileobj:
        json.dump(blogposts, fileobj, indent=4)

    return redirect("/")


@app.route("/update/<int:post_id>", )
def update(post_id):

    # Fetch the blog posts from the JSON file
    post, index = fetch_post_by_id(post_id)

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':

        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        id = post_id
        uuid = post["uuid"]

        try:
            with open("blogposts.json", "r") as fileobj:
                blogposts = json.load(fileobj)
        except FileNotFoundError:
            blogposts = []

        # Create a new blog post and add it to the list
        updated_post = {
            "id": id,
            "uuid": uuid,
            "author": author,
            "title": title,
            "content": content
            }

        blogposts[index] = updated_post

        with open("blogposts.json", "w") as fileobj:
            json.dump(blogposts, fileobj, indent=4)

        # Redirect to the home page
        return redirect(url_for('index'))

        # Update the post in the JSON file
        # Redirect back to index

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(port=5001)
