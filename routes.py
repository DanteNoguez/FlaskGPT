from flask import Flask, render_template, request, Response

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI

import unstructured 
import os
import openai
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
persist_directory = 'database/'
docsearch = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

def gen_prompt(docs, query) -> str:
    return f"""To answer the question please only use the Context given, nothing else. Do not make up answer, simply say 'I don't know' if you are not sure.
Question: {query}
Context: {[doc.page_content for doc in docs]}
Answer:
"""

def prompt(query):
     docs = docsearch.similarity_search(query, k=4)
     prompt = gen_prompt(docs, query)
     return prompt


def stream(input_text):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": "You're an assistant."},
            {"role": "user", "content": f"{prompt(input_text)}"},
        ], stream=True, max_tokens=500, temperature=0)
        for line in completion:
            if 'content' in line['choices'][0]['delta']:
                yield line['choices'][0]['delta']['content']

@app.route('/completion', methods=['GET', 'POST'])
def completion_api():
    if request.method == "POST":
        data = request.form
        input_text = data['input_text']
        return Response(stream(input_text), mimetype='text/event-stream')
    else:
        return Response(None, mimetype='text/event-stream')
    
if __name__ == '__main__':
    app.run(debug=True)

