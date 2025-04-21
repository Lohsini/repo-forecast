import os
from flask import Flask,Response,jsonify, render_template ,logging,request
app = Flask(__name__)

@app.route('/') 
def home():
    return render_template('index.html')

#run server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
