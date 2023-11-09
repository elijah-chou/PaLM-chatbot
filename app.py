from flask import Flask, request, render_template
import requests
import google.generativeai as palm
import config

palm.configure(api_key=config.api_key)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        message = request.form.get('message')
        response = send_to_palm_api(message)
        return render_template('response.html', response=response)
    return render_template('index.html')

def send_to_palm_api(message):
    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
    model = models[0].name
    prompt = """
    You are an expert at solving word problems.

    Solve the following problem:

    I have three houses, each with three cats.
    each cat owns 4 mittens, and a hat. Each mitten was
    knit from 7m of yarn, each hat from 4m.
    How much yarn was needed to make all the items?

    Think about it step by step, and show your work.
    """

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        # The maximum length of the response
        max_output_tokens=800,
    )
    return completion.result

if __name__ == '__main__':
    app.run(debug=True, port=8080)