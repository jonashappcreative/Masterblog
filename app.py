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
            json.dump(blogposts, fileobj, indent=4)

        # Redirect to the home page
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
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

    deleted_post = blogposts.pop(index_to_pop)

    print(f"Deleted Blog Post: \n{deleted_post}")

    with open("blogposts.json", "w") as fileobj:
        json.dump(blogposts, fileobj, indent=4)

    return redirect("/")


if __name__ == '__main__':
    app.run(port=5001)