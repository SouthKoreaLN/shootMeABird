# shootMeABird

We build this tool as a telegram bot (t.me/shootMeABirdBot).

The user can type any of the following commands to interact with the bot:
- /test
- /request_waifu
- /get_waifu
- ...

The latter command will ask the user to type the name of any object he would like to get an image of.

Once the user has typed this command, he will be prompted with a lightning network invoice to be paid.

Until the user pays the invoice (for instance, using his LN-enabled Bitcoin Wallet or using htlc.me), he is prompted with "you didn't pay the invoice yet" message.

Once he pays, the bot querries the GAN generator API to return us an image of the requested object. If the message is empty, a mushroom will be returned.

# GAN Info

Uses BigGAN from
https://github.com/huggingface/pytorch-pretrained-BigGAN.git and
styleGAN https://github.com/NVlabs/stylegan with Gwern's
ThisWaifuDoesNotExist model. Need to link the config/ and dnnlib/ from
styleGAN into the GAN/ directory.
