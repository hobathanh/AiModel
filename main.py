import os
from flask import Flask, request
from flask_restful import Resource, Api

from json import dumps
from flask import jsonify
from werkzeug.utils import secure_filename
from ImgCaptionModel import *
import random
UPLOAD_FOLDER = 'image'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api = Api(app)
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
class Tracks(Resource):
    def get(self):
        result = "ttt"
        return jsonify(result)

class predict(Resource):
    def post(self):
        if request.method == 'POST':
        # check if the post request has the file part
            if 'file' not in request.files:
                result = "No file part"
                return jsonify(result)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                result = "No file selected"
                return jsonify(result)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # result = "yes"
                image_path = "image/"+ filename
                result = evaluate_Predict(image_path)
                result = ' '.join(result)
                result = result.replace(' <end>','')
                                
                # declaring list
                # list = ['a', 'b', 'c', 'd', 'e', 'f']
                dbfile = open("train_captions", 'rb')      
                list = pickle.load(dbfile)  
                dbfile.close()
                # initializing the value of n
                import random
                list = random.sample(train_captions, 3)
                list.append(result)
                list = [s.replace(" <end>", "") for s in list]
                list = [s.replace("<start>  ", "") for s in list]
                list = [s.replace(" .", "") for s in list]
                list = random.sample(list,4)
                # list = [s.replace("<end>", "") for s in list]
                # list = [s.replace("<start>", "") for s in list]
                # result2 = ' '.join(result)
                # result = {'caption': result2, 'caption_split': result1}
                result = jsonify(
                    answer = result,
                    choices = list
                )
                result.headers.add('Access-Control-Allow-Origin', '*')
                return result
        return ''

api.add_resource(Tracks, '/tracks')
api.add_resource(predict, '/predict')
if __name__ == '__main__':
     app.run()


