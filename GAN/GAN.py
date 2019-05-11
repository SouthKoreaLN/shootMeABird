import torch
from pytorch_pretrained_biggan import (BigGAN, one_hot_from_names, truncated_noise_sample,
                                       save_as_images, display_in_terminal, convert_to_images)
import os
from quart import Quart, send_file, request, make_response

app = Quart(__name__)

models = {
    "biggan-deep-512" : BigGAN.from_pretrained('biggan-deep-512'),
    "biggan-deep-256" : BigGAN.from_pretrained('biggan-deep-256')
}

def get_model(name="biggan-deep-256"):
    "Get the deep model from known models"
    return models[name]

img_i = 0
def generate_image(thing="mushroom", model_name="biggan-deep-512", truncation=0.4):
    "Generate an image of *thing* from the model, save it and return the path"
    global img_i
    model = get_model(model_name)
    
    # Prepare a input
    truncation = 0.7
    class_vector = one_hot_from_names([thing], batch_size=1)
    noise_vector = truncated_noise_sample(truncation=truncation, batch_size=1)

    # All in tensors
    noise_vector = torch.from_numpy(noise_vector)
    class_vector = torch.from_numpy(class_vector)

    # If you have a GPU, put everything on cuda
    noise_vector = noise_vector.to('cuda')
    class_vector = class_vector.to('cuda')
    model.to('cuda')

    # Generate an image
    with torch.no_grad():
        output = model(noise_vector, class_vector, truncation)

    # If you have a GPU put back on CPU
    output = output.to('cpu')
    img = convert_to_images(output)
    out = img[0]
    file_name = f"images/{img_i}.png"
    img_i += 1
    os.system("mkdir -p images/")
    out.save(file_name, 'png')
    print(f"Generated an image of {thing} in file {file_name}")
    return file_name

@app.route('/')
def image_request():
    thing = request.args.get('thing') or "mushroom"
    truncation = request.args.get('truncation') or 0.7
    try:
        filename = generate_image(thing=thing, truncation=truncation)
    except:
        return make_response(("Can't generate image", 502))
    return send_file(filename, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
    # print("Generating a test image")
    # print(generate_image("lamp"))
