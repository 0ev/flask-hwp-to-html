from flask import Flask, render_template, request,send_from_directory,render_template_string,flash
from werkzeug.utils import secure_filename
from hwptohtml import change_to_html
import os
import stat
st = os.stat('/app/static/hwp5html.exe')
os.chmod('/app/static/hwp5html.exe', st.st_mode | stat.S_IEXEC)

ALLOWED_EXTENSIONS = {'hwp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
@app.route('/upload')
def render_file():
    return render_template('uploading.html')


@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if allowed_file(f.filename):
            f.save('/app/static/tempfile/'+secure_filename(f.filename))

            a=change_to_html('/app/static/tempfile/'+secure_filename(f.filename))

            return render_template_string(open("/app/static/tempfile/"+a+"/result.html",'r',encoding='UTF8').read())
        else:
            return render_template('uploading.html')

if __name__ == '__main__':
    app.run(debug = True)
