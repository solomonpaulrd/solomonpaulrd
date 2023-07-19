import openai
from flask import Flask, render_template, request

openai.api_key = "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"  # Replace with your OpenAI API key
app = Flask(__name__)
answer = None  # Initialize answer variable

def get_completion(prompt, model='gpt-3.5-turbo'):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    if response.choices and response.choices[0].message:
        return response.choices[0].message.get("content", "").strip()
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def home():
    global answer  # Use global answer variable

    if request.method == "POST":
        # Get uploaded CSV file
        csv_file = request.files["csv_file"]
        csv_data = csv_file.read().decode("utf-8")

        # Get prompt from the form
        prompt = request.form["prompt"]

        # Set the prompt with the CSV data
        prompt += f"\n\nCSV data:\n{csv_data}"

        # Get the answer using the OpenAI API
        answer = get_completion(prompt)

        if answer is None:
            error_message = "No answer available. Please check your prompt and try again."
            return render_template("index.html", error=error_message, answer=None)

    # Render the home page without a result or error initially
    return render_template("index.html", error=None, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
