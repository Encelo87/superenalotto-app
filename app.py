from flask import Flask, render_template_string
import random
import requests
from bs4 import BeautifulSoup
from collections import Counter

app = Flask(__name__)

URL = "https://www.superenalotto.it/archivio-estrazioni"

def prendi_dati():
    numeri = []
    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, "html.parser")

        estrazioni = soup.find_all("div", class_="draw")
        for e in estrazioni:
            nums = e.find_all("span", class_="number")
            row = [int(n.text) for n in nums[:6]]
            numeri.extend(row)
    except:
        pass

    return numeri

def statistiche():
    dati = prendi_dati()
    conteggio = Counter(dati)
    piu_frequenti = conteggio.most_common(10)
    return piu_frequenti

def genera_numeri():
    return sorted(random.sample(range(1, 91), 6))

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SuperEnalotto App</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial; text-align: center; background: #f4f4f4; }
        h1 { color: #333; }
        button { padding: 10px 20px; margin: 10px; }
        canvas { max-width: 600px; margin: auto; }
    </style>
</head>
<body>
    <h1>SuperEnalotto Dashboard</h1>

    <form method="post">
        <button name="azione" value="genera">Genera numeri</button>
    </form>

    {% if numeri %}
        <h2>{{ numeri }}</h2>
    {% endif %}

    <h2>Numeri più frequenti</h2>
    <canvas id="chart"></canvas>

    <script>
        const data = {{ stats|safe }};
        const labels = data.map(x => x[0]);
        const values = data.map(x => x[1]);

        new Chart(document.getElementById("chart"), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Frequenza',
                    data: values
                }]
            }
        });
    </script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    numeri = None
    if True:
        numeri = genera_numeri()

    stats = statistiche()

    return render_template_string(HTML, numeri=numeri, stats=stats)

if __name__ == "__main__":
    app.run()
