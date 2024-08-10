

# import flask important packages

import  sys
from pathlib import Path
base_dir = Path('/Web_Dev_AI')
sys.path.append(str(base_dir))

from flask import Flask, render_template, jsonify, request, flash
from inference_yolov7 import *

from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
'''
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

'''



class yolov7_json_handle:
    
    
    def __init__(self):
        
        self.template_dir = 'templates'
        self.static_folder = 'static'
        
        self.app = Flask(__name__, template_folder=self.template_dir, static_folder = self.static_folder)
        
        # sql dev config
        
        
        self.app.secret_key = "dlserverwebbapp"
        
    
        #=========JWT MANAGER===================#
        CORS(self.app)      
        
        # creata user table
      
        
        self.UPLOAD_FOLDER = 'static/uploads/'
        
        # app config
        self.app.config['UPLOAD_FOLDER'] = self.UPLOAD_FOLDER
        
        
        self.uploaded_file_path = None
        self.last_uploaded_files = []
        self.uploaded_file_path = None 
        
        
        self.ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
        
       
        self.path_to_classes =  'models/coco-classes.txt'
        self.image_path ='static/images'
        self.path_to_cfg_yolov7 = 'models/yolov7-tiny.cfg'
        self.path_to_weight_yolov7 ='models/yolov7-tiny.weights'
        self.flask_path = 'static/uploads'
        
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)


        self.app.add_url_rule('/Web_Dev_AI/main', view_func = self.main)
    
        
        #self.app.add_url_rule('/Web_Dev_AI/sign', view_func = self.sign, methods=['GET','POST'])
        
        
        #self.app.add_url_rule('/Web_Dev_AI/registration', view_func = self.registration, methods=['GET', 'POST'])
        
        
        self.app.add_url_rule('/Web_Dev_AI/system-works', view_func = self.system_works)
        
        self.app.add_url_rule('/Web_Dev_AI/dl-inference', view_func = self.dl_inference)
        
        # RENDER JSON OBJECT DETECTION
        self.app.add_url_rule('/Web_Dev_AI/process-data', view_func=self.render_postproces, methods=['POST'])
        
        self.app.add_url_rule('/Web_Dev_AI/dl-image-inference', view_func = self.dl_image_inference, methods = ['POST', 'GET'])
        
        self.app.add_url_rule('/Web_Dev_AI/last-uploaded', view_func = self.getlastFile, methods=['GET'])
            
        self.app.add_url_rule('/Web_Dev_AI/about-me', view_func = self.about_me)

    
     # ALLOWED FILE    
    def allowed_file(self, filename):
        
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    
    def main(self):
        
        return render_template('main.html')
    

    '''
    def sign(self):
        
        try:
            if request.method=='GET':
                return render_template('sign.html')  # Render the sign-in form for GET requests
           
            elif request.method=='POST':
                
                username = request.form['username']
                password = request.form['password']
                
                if not username or not password:
                    return jsonify({"error":"Username and Password are required!"}), 400
                
                user = User.query.filter_by(username=username).first()
               
                if user and check_password_hash(user.password, password=password):
                   
                    return jsonify({"success": "Logged in successfully!, Enjoy DL Inference"}), 200
                
                else:
                   return jsonify({"error": "Failed to Log In, please try again!"}), 401
            
        except Exception as e:
            print(f"Error during sign in operation {e}")
            return jsonify({"error":"Internal  Server Error"}), 500
            
       
    def registration(self):
        if request.method == 'GET':
            return render_template('registration.html')
        
        elif request.method=='POST':
            
            username = request.form.get('username')
            email = request.form.get('email')
            password =  request.form.get('password')
            password_confirm = request.form.get('password_confirm')
            
            
            print(f"Username : {username}, Email : {email}, password : {password}")
            
            if not username or not email or not password:
                # server cannot or will not process the request due to something that is perceived to be a client error
                return jsonify({"Error" : "SignUp Info Missing..."}), 400
            elif password != password_confirm:
                
                return jsonify({"Error":"Passwords do not match!"}), 400
        
            
            user_exists = User.query.filter_by(username=username).first()
            if user_exists:
                return jsonify({"Error": "User Already Exist, try with another username"}), 409
            
            hashed_password = generate_password_hash(password) 
            new_user = User(username=username, email=email, password=hashed_password)
            new_user.save_username()
            
                
            return jsonify({"Success" : "Succesfull Registration.."}), 201
        
    '''
    
    def system_works(self):
        return render_template('system_works.html')
    
    def dl_inference(self):
        return render_template('dl_inference.html')
    
    def about_me(self):
        return render_template('about_me.html')
    
    
    def dl_image_inference(self):
        if request.method == 'POST':
           
            file = request.files['image_name']
            
            if file and self.allowed_file(file.filename):
                
                filename = secure_filename(file.filename)
                # get file name
                self.last_uploaded_files.append(filename)
                
                if not os.path.exists(self.app.config['UPLOAD_FOLDER']):
                    
                    os.makedirs(self.app.config['UPLOAD_FOLDER'])
                    
                file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
                
                file.save(file_path)
               # print('**************',file_path, filename)
                processor_inference = Yolov7Processor(0.3, 0.38, self.path_to_classes, file_path, self.path_to_cfg_yolov7, self.path_to_weight_yolov7,
                                                      single_image=True)
               
                getImagesInference = processor_inference.inference_image_run(file_path)
              
                if getImagesInference:
                    # Convert to relative paths
                    relative_paths = [os.path.relpath(img_path) for img_path in getImagesInference]
                    flash('File successfully uploaded')
                    return render_template('dl_image_inference.html',   upload=True, upload_image=relative_paths)
                    
              
        
        return render_template('dl_image_inference.html', upload=False)
    
    
    def getlastFile(self):
        
        print("LAST UPLOAD", self.last_uploaded_files)
        
        return jsonify(self.last_uploaded_files)
        
     
    def render_postproces(self):
        
        try:
            processor = Yolov7Processor(0.3, 0.38, self.path_to_classes, self.image_path, self.path_to_cfg_yolov7, self.path_to_weight_yolov7)
            data = processor.convert_results_to_json()
            return jsonify(data)

        except Exception as e:
            print("Error", e)
            return str(e)
        


if __name__ == "__main__":
    yolov7_flask =  yolov7_json_handle()
   
    yolov7_flask.app.run(debug=True)
        
        
        