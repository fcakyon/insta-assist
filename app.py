from flask import Flask, request, jsonify, render_template
from utils import load_json
import config


app = Flask(__name__)


@app.route("/")
def hello():
    liked_media_dict = load_json(config.json_path)
    liked_media_list = liked_media_dict["clean"]
    # liked_media_list = liked_media_dict

    def sort_function(e):
        return e["timestamp"]

    liked_media_list.sort(reverse=True, key=sort_function)
    return render_template("index.html", liked_media_list=liked_media_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
