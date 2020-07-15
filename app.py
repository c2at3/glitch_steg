from flask import (Flask, render_template, request, url_for, redirect, send_from_directory, url_for)
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect


import os
import random

from Steg.LSB_StegImage import *

app = Flask(__name__)
app.debug = True
app.secret_key='tranbaquang'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'bmp', 'svg', 'tif', 'tiff', 'ico', 'png',
                    'jpg', 'jpeg', 'gif', 'pjp', 'pjpeg', 'jfif',
                    'svgz', 'xbm', 'dib', 'webp'}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024 #max = 10mb
app.config["CLIENT_IMAGES"] = 'static/hide'

csrf = CSRFProtect(app)
csrf.init_app(app)

def allowed_image_file(filesize):
    if int(filesize) <= app.config["MAX_CONTENT_LENGTH"]:
        return True
    return False

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/download/<string:filename>')
def download_file(filename):
    return send_from_directory(app.config["CLIENT_IMAGES"], filename=filename, as_attachment=True)

@app.route('/', methods=["POST", "GET"])
def main():
    form_name = ''
    folder_hide = 'static/hide'
    for f in os.listdir(app.config["UPLOAD_FOLDER"]):         
        os.remove('/'.join([app.config["UPLOAD_FOLDER"], f]))
    for f in os.listdir(folder_hide):         
        os.remove('/'.join([folder_hide, f]))    
    if request.files:
        if request.method == "POST":
            print(request.form)
            
            # Giấu tin
            if 'messageHide' in request.form:
                form_name = 'messageHide'
                if not allowed_image_file(request.cookies.get('filesize')):
                    print('File vượt quá kích thước, Kích thước tối đa 10MB')
                    return redirect(request.url)
                file = request.files['fileName']
                message = request.form.get('messageHide')
                print(message)
                if file.filename == '':
                    print('Chưa chọn file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    file_name = secure_filename(file.filename)
                    str = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMM'
                    id_image = random.choices(str, k=12)
                    id_image = ''.join(id_image)
                    new_fileName = id_image + '.png'
                    image_path = '/'.join([app.config["UPLOAD_FOLDER"], id_image + '.png'])
                    print(image_path)
                    file.save(image_path)
                    hide = HidePrivate(message, image_path)
                    hide.hideNormal(new_fileName);
                    print('static/hide/{}'.format(new_fileName))
                    nameFile, = os.listdir('static/hide')
                    link_file = url_for("static", filename='hide/{}'.format(nameFile))
                    print(link_file)
                    
                    show = GetMessageHide('static/hide/{}'.format(new_fileName), 100)
                    print(show.getMessageHideNormal())
                    return render_template('index.html', image_path=image_path, link_file=link_file, nameFile=nameFile, form_name=form_name)
                else:
                    print('File không hợp lệ!')
                    return redirect(request.url)
            #END giấu tin
            
            # Giải mã tin
            if 'numberPixelScan' in request.form:
                print('Đã vô')
                form_name = 'numberPixelScan'
                if not allowed_image_file(request.cookies.get('filesize')):
                    print('File vượt quá kích thước, Kích thước tối đa 10MB')
                    return redirect(request.url)
                file = request.files['fileName']
                number_scan = request.form.get('numberPixelScan')
                try:
                    number_scan = int(number_scan)
                    print(number_scan)
                    if file.filename == '':
                        print('Chưa chọn file')
                        return redirect(request.url)
                    if file and allowed_file(file.filename):
                        file_name = secure_filename(file.filename)
                        str = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMM'
                        id_image = random.choices(str, k=12)
                        id_image = ''.join(id_image)
                        new_fileName = id_image + '.png'
                        image_path = '/'.join(['static/hide', id_image + '.png'])
                        print(image_path)
                        file.save(image_path)
                            
                        show = GetMessageHide('static/hide/{}'.format(new_fileName), number_scan)
                        data = show.getMessageHideNormal()
                        return render_template('index.html', image_path=image_path, data=data, form_name=form_name)
                    else:
                        print('File không hợp lệ!')
                        return redirect(request.url)
                except Exception:
                    print('Số lượng scan không hợp lệ!')
                    return redirect(request.url)
            # END Giải mã tin
        
    return render_template('index.html')

