from flask import Flask, render_template

app = Flask(__name__)

taches = ["faire les courses", "faire le ménage", "faire la vaisselle"]

@app.route('/')
def index():
    return render_template('index.html', taches=taches)

if __name__ == '__main__':
    app.run(debug=True)