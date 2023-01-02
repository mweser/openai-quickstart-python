import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    prompt_to_render = ""
    if request.method == "POST":
        in_prompt = request.form["prompt_field"]
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=in_prompt,
            temperature=0,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        usage_obj = response.usage

        usage_str = f'TOKEN USAGE (Model: {response.model})\n' \
                    f'Prompt:\t\t{usage_obj.prompt_tokens}\n' \
                    f'Completion:\t{usage_obj.completion_tokens}\n' \
                    f'Total:\t\t{usage_obj.total_tokens}'

        print(usage_str)
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    print(result)
    return render_template("index.html", result=result, your_input=prompt_to_render)


def codegen_prompt(language):
    return f'Generate a hello world program in {language}'


def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )
