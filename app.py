from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():

    # add code here to fetch the job posts from a file

    with open("blogposts.json", "r") as fileobj:
        blogposts = json.load(fileobj)

    return render_template("index.html", data=blogposts)


def main():

    with open("blogposts.json", "r") as fileobj:
        blogposts = json.load(fileobj)
        print(type(blogposts))

    for blogpost in blogposts:
        print(blogpost["id"])
        print(blogpost["author"])
        print(blogpost["title"])
        print(blogpost["content"])


if __name__ == '__main__':
    """
    Switch between main and app.run for debugging purposes
    main is for debugging
    app.run is for running the server
    """
    # main()
    app.run(port=5001)
