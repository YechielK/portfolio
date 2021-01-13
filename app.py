from lib.predict import predict
from flask import Flask, request, render_template, g, session
import bayesian
import rsa
app = Flask(__name__)

app.config["SECRET_KEY"] = "open secret"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')

@app.route('/projects', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('projects.html')

@app.route("/sentiment_predictor")
def sentiment_predictor():
    return render_template('sentiment_predictor.html')

@app.route("/predict")
def predict_route():
    sentence = request.args.get("sentence")
    output = predict(sentence)
    if output == 1:
        output = "Positive"
        prob = g.model.predict_proba(g.X).round(3)[0][1]
    else:
        output = "Negative"
        prob = g.model.predict_proba(g.X).round(3)[0][0]
    return render_template('sentiment_predictor.html', result=output, sentence=sentence, lemmed=g.lemmed, prob=prob, showPrediction=True)

@app.route('/chessboard_code', methods=['GET', 'POST'])
def chessboard_code():
    if request.method == 'GET':
        return render_template('chessboard.html')

@app.route('/bayesian_calculator', methods=['GET', 'POST'])
def bayesian_calculator():
    if request.method == 'GET':
        return render_template('bayes.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'GET':
        a = request.args.get("name_a")
        b = request.args.get("name_b")
        x = request.args.get("a")
        y = request.args.get("bga")
        z = request.args.get("bgna")
        
        values = bayesian.calculate(x,y,z)

        return render_template('bayes.html', v=values, a=a, b=b)

@app.route('/rsa_encryption', methods=['GET', 'POST'])
def rsa_encryption():
    if request.method == 'GET':
        return render_template('rsa.html')

@app.route('/calculate_rsa', methods=['GET', 'POST'])
def calculate_rsa():
    if request.method == 'GET':
        # msg = str(request.args.get("msg"))
        p = int(request.args.get("p"))
        q = int(request.args.get("q"))

        # if msg == "":
        keys = rsa.get_keys(p,q)
        session['keys'] = keys
        # print(session['keys'])
        return render_template('rsa.html', k=keys)

        # dict = rsa.calculate(msg, p, q)
        # print(dict)
        # return render_template('rsa.html', d=dict)

@app.route('/calculate_msg', methods=['GET', 'POST'])
def calculate_msg():
    if request.method == 'GET':
        msg = str(request.args.get("msg"))
        print(session['keys'])

        dict = rsa.calculate(msg, session['keys']['p'], session['keys']['q'])
        print(dict)
        return render_template('rsa.html', k=session['keys'], d=dict)



