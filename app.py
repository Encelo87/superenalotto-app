from flask import Flask, render_template_string, request
import random
import requests
from bs4 import BeautifulSoup
from collections import Counter

app = Flask(__name__)

URL = "https://www.superenalotto.it/archivio-estrazioni"

def prendi_dati():
    numeri = []
    estrazioni_complete = []

    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, "html.parser")

        estrazioni = soup.find_all("div", class_="draw")

        for e in estrazioni:
            nums = [int(n.text) for n in e.find_all("span", class_="number")[:6]]
            numeri.extend(nums)
            estrazioni_complete.append(nums)

    except:
        pass

    return numeri, estrazioni_complete


def statistiche():
    numeri, estrazioni = prendi_dati()
    conteggio = Counter(numeri)

    frequenti = conteggio.most_common(10)

    # ritardatari
    ultimi = estrazioni[-20:] if len(estrazioni) > 20 else estrazioni
    usciti_recenti = set(n for estr in ultimi for n in estr)

    ritardatari = [n for n in range(1, 91) if n not in usciti_recenti][:10]

    return frequenti, ritardatari, estrazioni[-5:]


def genera_intelligente():
    numeri = random.sample(range(1, 91), 6)

    # bilanciamento pari/dispari
    pari = [n for n in numeri if n % 2 == 0]
    dispari = [n for n in numeri if n % 2 != 0]

    while not (2 <= len(pari) <= 4):
        numeri = random.sample(range(1, 91), 6)
        pari = [n for n in numeri if n % 2 == 0]

    return sorted(numeri)


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>SuperEnalotto PRO</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body { font-family: Arial; background:#121212; color:white; text-align:center; }
button { padding:10px; margin:10px; border:none; background:#00c853; color:white; cursor:pointer; }
.card { background:#1e1e1e; padding:15px; margin:10px; border-radius:10px; }
</style>
</head>

<body>

<h1>🎯 SuperEnalotto PRO</h1>

<form method="post">
<button name="azione" value="genera">🎲 Genera numeri</button>
</form>

{% if numeri %}
<div class="card">
<h2>{{ numeri }}</h2>
</div>
{% endif %}

<div class="card">
<h3>📊 Numeri frequenti</h3>
<canvas id="freq"></canvas>
</div>

<div class="card">
<h3>⏳ Ritardatari</h3>
<p>{{ ritardatari }}</p>
</div>

<div class="card">
<h3>📅 Ultime estrazioni</h3>
{% for e in estrazioni %}
<p>{{ e }}</p>
{% endfor %}
</div>

<script>
const freq = {{ frequenti|safe }};
new Chart(document.getElementById("freq"), {
type: 'bar',
data: {
labels: freq.map(x=>x[0]),
datasets:[{data: freq.map(x=>x[1])}]
}
});
</script>

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def home():
    numeri = None

    if request.method == "POST":
        numeri = genera_intelligente()

    frequenti, ritardatari, estrazioni = statistiche()

    return render_template_string(HTML,
        numeri=numeri,
        frequenti=frequenti,
        ritardatari=ritardatari,
        estrazioni=estrazioni
    )

if __name__ == "__main__":
    app.run()
