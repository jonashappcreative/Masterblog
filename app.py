from flask import Flask, render_template, request, redirect, url_for
import json
import uuid

app = Flask(__name__)

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
            json.dump(blogposts, fileobj)

        # Redirect to the home page
        return redirect(url_for('index'))

    return render_template('add.html')


if __name__ == '__main__':
    app.run(port=5001)