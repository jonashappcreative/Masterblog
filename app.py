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
            post = blogposts[index_of_post]
            return post, index_of_post
        else:
            continue

    print("Post not in Posts")


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

    post, index = fetch_post_by_id(post_id)
    del blogposts[index]

    print(f"Deleted Blog Post: \n{post}")

    with open("blogposts.json", "w") as fileobj:
        json.dump(blogposts, fileobj, indent=4)

    return redirect("/")


@app.route("/update/<int:post_id>", methods=['GET', 'POST'])
def update(post_id):
    post, index = fetch_post_by_id(post_id)

    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        updated_post = {
            "id": post_id,
            "uuid": post["uuid"],  # Preserve the original UUID
            "author": author,
            "title": title,
            "content": content
        }

        try:
            with open("blogposts.json", "r") as fileobj:
                blogposts = json.load(fileobj)
            blogposts[index] = updated_post
            with open("blogposts.json", "w") as fileobj:
                json.dump(blogposts, fileobj, indent=4)
        except (FileNotFoundError, IndexError):
            return "Error updating the post", 500

        # Redirect to the home page after successful update
        return redirect(url_for('index'))

    # For GET request, render the update page with the existing post data
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(port=5001)
