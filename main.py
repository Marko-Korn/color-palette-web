from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename
from PIL import Image
import os
import numpy as np

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Bootstrap5(app)


# Check if an extension is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(fullpath)
            palette_hex, palette_rgb = get_colors_in_image(fullpath)
            return redirect(url_for('image_page.html', name=filename, hex_success=True,
                                    palette_hex=palette_hex, palette_rgb=palette_rgb))
    return render_template("index.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == "POST":
        f = request.files['file']
        filename = secure_filename(f.filename)

    if len(filename) > 1:
        fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(fullpath)
        palette_hex, palette_rgb = get_colors_in_image(fullpath)
        return render_template("image_page.html", hex_success=True, palette_hex=palette_hex,
                               palette_rgb=palette_rgb, name=f.filename)
    return render_template("index.html", name=f.filename)


def get_colors_in_image(filepath):
    def rgb_to_hex(r, g, b):
        ans = ('{:X}{:X}{:X}').format(r, g, b)

        while len(ans) < 6:
            ans = "0" + ans

        return "#" + ans

    def hex_to_rgb(h):
        rgb = []
        for i in (0, 2, 4):
            decimal = int(h[i:i + 2], 16)
            rgb.append(decimal)

        return tuple(rgb)

    def get_top_10(hex_list):
        hex_frequency = {}

        for item in hex_list:
            if item in hex_frequency:
                hex_frequency[item] += 1
            else:
                hex_frequency[item] = 1

        sorted_hex = dict(sorted(hex_frequency.items(), key=lambda item: item[1]))

        return list(sorted_hex.keys())[-10:][::-1]

    image_file = Image.open(filepath)
    image_array = np.array(image_file)

    shape = image_array.shape

    x = shape[0]
    y = shape[1]

    hex_list = []
    for x in range(x):
        for y in range(y):
            rgb = image_array[x, y, :]

            r = rgb[0]
            g = rgb[1]
            b = rgb[2]

            hex_list.append(rgb_to_hex(r, g, b))

    top_10_hex = get_top_10(hex_list)
    top_10_rgb = [hex_to_rgb(i[-6:]) for i in top_10_hex]

    return top_10_hex, top_10_rgb


if __name__ == "__main__":
    app.run(debug=True, port=5001)