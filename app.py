from flask import Flask,render_template,url_for,request,jsonify
import joblib
import re
import string
import pandas as pd

# Initialize the flask class and specify the templates directory
app = Flask(__name__,template_folder="templates")
Model = joblib.load('model.pkl')

# Default route set as 'home'
@app.route('/')
@app.route('/index')
def home():
    return render_template('Index.html') # Render home.html


def wordpre(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub("\\W"," ",text) # remove special chars
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

# Route 'classify' accepts GET request
@app.route('/predict',methods=['POST','GET'])
def classify_type():
    try:
        txt = request.form['text']
        txt = wordpre(txt)
        txt = pd.Series(txt)
        res = Model.predict(txt)
        if(res[0]==1):
            res="The news is REAL!!😃"
        else:
            res="The news is FAKE!!😨"
        return jsonify({'result':res})
    except:
        return 'Error' 

# Run the Flask server
if(__name__=='__main__'):
    app.run(debug=True)