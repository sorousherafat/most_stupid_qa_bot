from flask import Flask, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

df = pd.read_csv("qa.csv")


@app.route("/ping")
def ping():
    app.logger.debug("ping.")
    return "pong"


@app.route("/qa", methods=["POST"])
def qa():
    question = request.json["question"]
    qa = df.loc[df["question"] == question, "answer"]
    if qa.empty:
        app.logger.info(f"question: `{question}' was not found.")
        return "question not found", 404
    answer = qa.iloc[0]
    app.logger.debug(f"answered: `{answer}' to question: `{question}'")
    return {"answer": answer}


if __name__ == "__main__":
    app.run()
