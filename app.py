import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        news_url = request.form["url"]
        human = request.form["human"]
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(news_url),
        temperature=0.6
        )
        response2 = openai.Completion.create(
        model="text-davinci-003",
        prompt=generate_prompt(human),
        temperature=0.6
        )

        combinedGPTResponse = "Animal: " +  response.choices[0].text +  "\n\n Human:" + response2.choices[0].text
        return redirect(url_for("index", result=combinedGPTResponse))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(animal.capitalize())
