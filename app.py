import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

text_model = "text-davinci-002"
code_model = "code-davinci-002"

# frequency_penalty:
#
# Number between -2.0 and 2.0.
# Positive values penalize new
# tokens based on their existing
# frequency in the text so far,
# decreasing the model's likelihood
# to repeat the same line verbatim.

@app.route("/", methods=("GET", "POST"))
def index():
    horiz_line = "\n**************************\n"
    if request.method == "POST":
        in_prompt = request.form["prompt_field"]

        translate_to_kotlin_str = "Translate to Kotlin (use Exposed for database and do NOT use Android libraries)"
        translate_to_kotlin_str = ""

        prompt_full = f'"""' \
                      f'{in_prompt}' \
                      f'"""' \
                      f'\n\n {translate_to_kotlin_str}'

        print(f'{horiz_line}PROMPT:\n{prompt_full}{horiz_line}')

        response = openai.Completion.create(
            model=code_model,
            prompt=prompt_full,
            temperature=0,
            max_tokens=4000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            echo=False,

        )
        usage_obj = response.usage

        usage_str = f'TOKEN USAGE (Model: {response.model})\n' \
                    f'Prompt:\t\t{usage_obj.prompt_tokens}\n' \
                    f'Completion:\t{usage_obj.completion_tokens}\n' \
                    f'Total:\t\t{usage_obj.total_tokens}'

        print(f'{horiz_line}{usage_str}{horiz_line}')
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    print(f'RESULT:\n{result}{horiz_line}')
    return render_template("index.html", result=result)


seq_code_prompt = '''
"""
1. Prompt user to input a phone number
2. Prompt to input a nickname
3. Save results in a data class called Vendor
4. Save results to a sqlite database indexed by id
"""
'''

translation_prefix = f"Translate to French and preserve formatting:\n\n"

translation_example = {
    "model": "text-davinci-003",
    "prompt": "Translate this into 1. French, 2. Spanish and 3. Japanese and 4. Farsi:\n\nWhere do you live in the city?\n\n1.",
    "temperature": 0.3,
    "max_tokens": 100,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

unstructured_prompt = 'A table summarizing the fruits from Goocrux:\n\n' \
                      'There are many fruits that were found on the recently discovered ' \
                      'planet Goocrux. There are neoskizzles that grow there, which are ' \
                      'purple and taste like candy. There are also loheckles, which are a ' \
                      'grayish blue fruit and are very tart, a little bit like a lemon. ' \
                      'Pounits are a bright green color and are more savory than sweet. ' \
                      'There are also plenty of loopnovas which are a neon pink flavor and ' \
                      'taste like cotton candy. Finally, there are fruits called glowls, which ' \
                      'have a very sour and bitter taste which is acidic and caustic, and a pale orange ' \
                      'tinge to them.\n\n' \
                      '| Fruit | Color | Flavor |'

parse_unstructured_data = {
    "model": "text-davinci-003",
    "prompt": "A table summarizing the fruits from Goocrux:\n\nThere are many fruits that were found on the recently discovered planet Goocrux. There are neoskizzles that grow there, which are purple and taste like candy. There are also loheckles, which are a grayish blue fruit and are very tart, a little bit like a lemon. Pounits are a bright green color and are more savory than sweet. There are also plenty of loopnovas which are a neon pink flavor and taste like cotton candy. Finally, there are fruits called glowls, which have a very sour and bitter taste which is acidic and caustic, and a pale orange tinge to them.\n\n| Fruit | Color | Flavor |",
    "temperature": 0,
    "max_tokens": 100,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
}

text2Cmd = {
    "model": "text-davinci-003",
    "prompt": "Convert this text to a programmatic command:\n\nExample: Ask Constance "
              "if we need some bread\nOutput: send-msg `find constance` Do we need some bread?\n\n"
              "Reach out to the ski store and figure out if I can get my skis fixed before "
              "I leave on Thursday",
    "temperature": 0,
    "max_tokens": 100,
    "top_p": 1,
    "frequency_penalty": 0.2,
    "presence_penalty": 0
}


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
