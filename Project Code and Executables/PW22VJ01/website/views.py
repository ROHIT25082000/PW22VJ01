from flask import Blueprint
from flask import render_template, request, redirect, flash, send_file
from werkzeug.utils import secure_filename   
import random 
import os, shutil


ALLOWED_EXTENSIONS = {'csv'} 
UPLOAD_FOLDER = 'website/static/uploads'
DOWNLOAD_FOLDER = 'website/static/downloads'



views = Blueprint('views', __name__)

@views.route('/')
def home_page(): 
    try:
        clear_files()
    except Exception as e: 
        print("There was an issue in spawning subprocess\n" + str(e))
    return render_template('index.html') 

@views.route('/about') 
def about_us():  
    values = [1, 2, 3]  
    value_passed = random.choice(values)
    return render_template('about.html', passed_value=value_passed) 


@views.route('/contact')
def contact():
    return render_template('contact.html')

######################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def clear_files():  
    folder = UPLOAD_FOLDER
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))



######################
@views.route('/engine' ,methods=['GET', 'POST']) 
def engineering():
    uploaded_file = 'No file uploaded'
    IsUploaded = False
    if request.method == 'POST':
        file = request.files['input_file']
        #file.save()
        if file.filename == '':
            flash("No file selected ", category='error')
            return redirect('/engine')

        if file and allowed_file(file.filename):
            try:
                clear_files()
            except Exception as e:
                print("There was an issue in spawning subprocess\n" + str(e))
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            uploaded_file = filename 
            IsUploaded = True
            flash("File uploaded successfully", category='message')
        else:
            flash("Please upload only .csv files ", category='error')
            return redirect('/engine')

        return render_template('engine.html', file_uploaded=uploaded_file, IsFile=IsUploaded)
    elif request.method == 'GET':
        return render_template('engine.html')

@views.route('/engine/run')
def run_models():
    tasks = True
    curr_path = os.getcwd()
    print(curr_path)
    os.chdir(curr_path + '/website/static/uploads')  
    ls = os.listdir()
    if len(ls) > 0:
        import subprocess as sp
        os.chdir(curr_path + '/website/static/')
        print(os.getcwd()) 
        try:
            
            sp.call("python3 breach_code.py", shell=True)
            sp.call("python3 creditcard.py", shell=True)
            sp.call("python3 selfdeliveryfraud.py",shell=True)

            print("Success but ran /engine/run ")
            tasks = False
        except Exception as e:
            print("There was an issue in spawning subprocess\n" + str(e))
    os.chdir(curr_path)
    if tasks:    
        return render_template('no_tasks.html', no_tasks=tasks)  
    else:   
        return render_template('downloads.html', manual_user=False)


@views.route('/downloads')
def downloads():
    user = True
    return render_template('downloads.html', manual_user = user)

@views.route('/download_files/<path:filename>')
def download_files(filename): 
    print(filename) 
    curr_path = os.getcwd() 
    path = curr_path + '/website/static/downloads/' + filename 
    print(path)
    return send_file(path, as_attachment=True)

@views.after_request
def cache_control(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response