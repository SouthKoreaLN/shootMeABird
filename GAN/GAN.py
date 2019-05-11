import torch
from pytorch_pretrained_biggan import (BigGAN, one_hot_from_names, truncated_noise_sample,
                                       save_as_images, display_in_terminal, convert_to_images)
import os
from quart import Quart, send_file, request, make_response

import os
import pickle
import numpy as np
import PIL.Image
import dnnlib
import dnnlib.tflib as tflib
import config
import random

app = Quart(__name__)
tflib.init_tf()

models = {
    "biggan-deep-512" : BigGAN.from_pretrained('biggan-deep-512'),
    "biggan-deep-256" : BigGAN.from_pretrained('biggan-deep-256'),
    "waifu" : pickle.load(open("2019-04-30-stylegan-danbooru2018-portraits-02095-066083.pkl", 'rb'))[-1],
    "celeb" : pickle.load(open("karras2019stylegan-celebahq-1024x1024.pkl", 'rb'))[-1]
}

def get_model(name="biggan-deep-256"):
    "Get the deep model from known models"
    return models[name]

def generate_waifu(model_name, truncation):
    global img_i
    model = get_model(model_name)
    rnd = np.random.RandomState(random.randint(1, 10000))
    latents = rnd.randn(1, model.input_shape[1])
    # gen image
    fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
    images = model.run(latents, None, truncation_psi=float(truncation), randomize_noise=True, output_transform=fmt)
    file_name = f"images/{img_i}.png"
    img_i += 1
    print(f"Generated waifu at {file_name}")
    PIL.Image.fromarray(images[0], 'RGB').save(file_name)
    return file_name

img_i = 0
def generate_image(thing="mushroom", model_name="biggan-deep-512", truncation=0.4):
    "Generate an image of *thing* from the model, save it and return the path"

    if model_name in ["waifu", "celeb"]: return generate_waifu(model_name, truncation)
    
    global img_i
    model = get_model(model_name)
    
    # Prepare a input
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
    print(f"Generated an image of {thing} in file {file_name} with model {model_name}")
    return file_name


import traceback

@app.route('/')
def image_request():
    thing = request.args.get('thing') or "mushroom"
    truncation = request.args.get('truncation') or 0.7
    model = request.args.get('model') or "waifu"
    try:
        print(f"{thing} {model} {truncation}")
        filename = generate_image(thing=thing, model_name=model, truncation=float(truncation))
    except:
        traceback.print_exc()
        return make_response(("Can't generate image", 502))
    return send_file(filename, mimetype="image/png")

if __name__ == "__main__":
    # Need to generate BigGAN first, otherwise waifu exhausts the GPU
    # memory (on my 1060 Ti)
    generate_image(model_name="biggan-deep-512")
    generate_image(model_name="waifu")
    app.run(debug=True)
    # print("Generating a test image")
    # print(generate_image("lamp"))
