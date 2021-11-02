import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def input_form():
    return render_template("index.html")

@app.route("/predict/", methods=['GET', 'POST'])
def predict():
    data = {"Code_commune": request.form["Code_commune"],
            "Nombre_de_lots": request.form["Nombre_de_lots"],
            "Type_local": request.form["Type_local"],
            "Surface_reelle_bati": request.form["Surface_reelle_bati"],
            "Surface_terrain": request.form["Surface_terrain"],
            "Nombre_pieces_principales": request.form["Nombre_pieces_principales"]}
    df = pd.DataFrame(data).astype(str)
    return type(df[0]["Code_commune"][0])

if __name__ == "__main__":
    app.run()