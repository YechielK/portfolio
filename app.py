from lib.predict import predict
from flask import Flask, request, render_template, g
import bayesian
app = Flask(__name__)

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
    # if request.method == 'POST':
    #     print("tester posr")
    #     # bayesian.calculate(request.args.get("a"))
    #     return render_template('bayes.html', foobar=values)

