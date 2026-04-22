from flask import Flask, render_template_string
import random

app = Flask(__name__)

def genera_numeri():
    return sorted(random.sample(range(1, 91), 6))

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SuperEnalotto App</title>
    <style>
        body { font-family: Arial; text-align: center; background: #f4f4f4; }
        h1 { color: #333; }
        button { padding: 10px 20px; font-size: 16px; }
        .box { margin-top: 20px; }
    </style>
</head>
<body>
    <h1>SuperEnalotto Generator</h1>
    <form method="post">
        <button type="submit">Genera numeri</button>
    </form>
    {% if numeri %}
    <div class="box">
        <h2>{{ numeri }}</h2>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    numeri = None
    if True:
        numeri = genera_numeri()
    return render_template_string(HTML, numeri=numeri)

if __name__ == "__main__":
    app.run()
