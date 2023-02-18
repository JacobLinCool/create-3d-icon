import time
import tempfile
import subprocess
from flask import Flask, request, send_file

app = Flask(__name__)


@app.route("/")
def alive():
    return send_file("ui.html")


@app.route("/create", methods=["POST"])
def create():
    data = request.get_json()

    if "svg" not in data:
        return "error"

    svg = data["svg"]

    # make a temp dir
    dir = tempfile.mkdtemp()
    filepath = dir + "/temp.svg"

    with open(filepath, "wb") as f:
        f.write(svg.encode("utf-8"))
        f.flush()

        rotate_x = data["rotate_x"] if "rotate_x" in data else 0
        rotate_y = data["rotate_y"] if "rotate_y" in data else 0
        rotate_z = data["rotate_z"] if "rotate_z" in data else 0
        thickness = data["thickness"] if "thickness" in data else 1
        distance = data["distance"] if "distance" in data else 1
        light_x = data["light_x"] if "light_x" in data else 0
        light_y = data["light_y"] if "light_y" in data else 0
        light_z = data["light_z"] if "light_z" in data else 0
        light_strength = data["light_strength"] if "light_strength" in data else 1
        color_r = data["color_r"] if "color_r" in data else -1
        color_g = data["color_g"] if "color_g" in data else -1
        color_b = data["color_b"] if "color_b" in data else -1
        size = data["size"] if "size" in data else 2048
        bevel = data["bevel"] if "bevel" in data else 1

        subprocess.run([
            "blender",
            "--background",
            "--python",
            "create.py",
            "--",
            filepath,
            "--rotate-x", str(rotate_x),
            "--rotate-y", str(rotate_y),
            "--rotate-z", str(rotate_z),
            "--thickness", str(thickness),
            "--distance", str(distance),
            "--light-x", str(light_x),
            "--light-y", str(light_y),
            "--light-z", str(light_z),
            "--light-strength", str(light_strength),
            "--red", str(color_r),
            "--green", str(color_g),
            "--blue", str(color_b),
            "--size", str(size),
            "--bevel", str(bevel)
        ])

    return send_file(dir + "/temp.png", mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
