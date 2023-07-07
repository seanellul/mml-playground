from flask import Flask, request, Response, jsonify, send_from_directory
# from flask_cors import CORS
import os
import openai
from configs.dataset import questions, answers

app = Flask(__name__)
# CORS(app)  # To allow requests from different origin (your MML document in this case)

global_message = "Chat GPT's Reply will Load Here"

@app.route('/get_variable', methods=['GET'])
def get_variable():
    global global_var
    return jsonify({'the_var': global_message})



@app.route('/process_input', methods=['POST'])
def process_input():
    global global_message
    user_input = request.json['user_input']
    print(f"Received user input: {user_input}")

    openai.api_key = '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'
    system = 'You are a helpful coding assistant, who will reply with possible code snippets for the new language LLM. You are only to reply using the following elements: <m-group> The m-group element can contain other MML tags, allowing all of them to be transformed as single item <m-cube> The m-cube element is a primitive 3D cube that can be coloured. It is often used for debugging or initial development purposes <m-sphere> The m-sphere element is a primitive 3D sphere that can be coloured. It is often used for debugging or initial development purposes <m-cylinder> The m-cylinder element is a primitive 3D cylinder that can be coloured. It is often used for debugging or initial development purposes <m-light> The m-light element is a light that supports various types (e.g. point, spotlight) and can be coloured <m-plane> The m-plane element is a primitive 3D plane that can be coloured <m-model> The m-model element is a 3D model. It can be used to load and display various 3D model file formats, such as OBJ, FBX, or GLTF, depending on the rendering engine being used. The model can be positioned, rotated, and scaled within the 3D scene. It also supports animations <m-character> The m-character element is a 3D character. It supports containing other m-model elements, allowing for composing a character from multiple models <m-frame> The m-frame element is a 3D frame. It enables composing other MML documents into the document and transforming them as a unit <m-audio> The m-audio element is used to play audio in a 3D scene <m-image> The m-image element is used to display an image in a 3D scene <m-video> The m-video element is used to display a video in a 3D scene <m-label> The m-label element is used to display text on a plane in a 3D scene <m-prompt>The m-prompt element is used to request a string from the user when the element is clicked in a 3D scene. <m-interaction>	The m-interaction element is used to describe an action that a user can take at a point in 3D space.'
    question = user_input

    completion = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {"role": "system", "content": system},
      {"role": "user", "content": questions[0]},
      {"role": "assistant", "content": answers[0]},
      {"role": "user", "content": questions[1]},
      {"role": "assistant", "content": answers[1]},
      {"role": "user", "content": questions[2]},
      {"role": "assistant", "content": answers[2]},
      {"role": "user", "content": questions[3]},
      {"role": "assistant", "content": answers[3]},
      {"role": "user", "content": questions[4]},
      {"role": "assistant", "content": answers[4]},
      {"role": "user", "content": questions[5]},
      {"role": "assistant", "content": answers[5]},
      {"role": "user", "content": questions[6]},
      {"role": "assistant", "content": answers[6]},
      {"role": "user", "content": questions[7]},
      {"role": "assistant", "content": answers[7]},
      {"role": "user", "content": questions[8]},
      {"role": "assistant", "content": answers[8]},
      {"role": "user", "content": question},
    ]
  )

    html = f"""
    {completion.choices[0].message.content}
    """


    global_message =  completion.choices[0].message.content

    # Write the response to 'duck.html' file
    with open('../packages/server/examples/test.html', 'w') as file:
        file.write(html)
    
    return jsonify({'response': 'duck.html updated'})  # Returns a JSON response

# @app.route('/packages/server/examples/test.html')
# def serve_file():
#     return send_from_directory(os.getcwd(), 'duck.html')

if __name__ == '__main__':
    app.run(port=5000)  # The server will be accessible at http://localhost:5000/
