Howdy friends, here's a guide on how to train the highest fidelity pitch model possible with DiffSinger!

(This guide is accurate as of April 27th 2024, things are bound to change in time with DiffSinger!)

### Things you need before you begin!
- A dataset with PROPERLY CONFIGURED PITCH! Yes, you need to [slurcut](https://github.com/openvpi/dataset-tools/releases/tag/20240426.0) your data, it's not difficult and will literally take you like an hour at most.
- A way to train DiffSinger. I highly recommend training locally because of the control it gives you, but if you cannot train locally, MLo7 has made some very nice Colab training notebooks!
- The slightest understanding of some specifics for training AI models.

***!!! DISCLAIMER !!!***

The quality of your pitch model _absolutely does rely_ on how good the singing in your data is. You can pitch correct pitch data, but if the singing is flat/unexpressive, that is what you will get with this. 
Since pitch models are optional, it's totally not something you need to deal with if you don't want to. But, having a good pitch model makes DiffSinger much more fun to use, in my opinion.
You can also steal pitch models for other speakers, which is something that I've done, so if you aren't the best singer but you have some data that is sang well, so long as the phonemes match up properly, you can use that one!

***!!! DISCLAIMER 2!!!***

You can absolutely try using [SOME](https://github.com/openvpi/SOME) to skip slurcutting, but you absolutely should still correct it. It's much better of a pitch extractor than **ParselMouth** or **RVMPE**, but it is nowhere near perfect.
If anything, you might get a better base, but you absolutely should still clean up the pitch configuration with slurcutter.

Link to MLo7's Training Notebook!

<a href="https://colab.research.google.com/github/MLo7Ghinsan/DiffSinger_colab_notebook_MLo7/blob/main/DiffSinger_colab_notebook.ipynb"> <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" style="width: 150px;"/> </a>

# Step 1: Preparing the data for training 📝

Usually when I train DiffSinger, I have 2 seperate datasets. 1) Training Data & 2) Pitch Data. Training Data has all of the data I'm training, and then Pitch Data is a much smaller subset of data that I've configured with Slurcutter to be able to actually train a pitch model.
A good rule of thumb is no less than 10% of the main data, depending on how much data you have. For example, TIGER all together has about 3 hours of ~~labelled~~ data, and his pitch models have about 30-40 minutes, give or take (I haven't actually timed it).

Once you have your properly converted datasets, set up as WAV + CSV or WAV + DS, you can move on to the next step!

# Step 2: Properly Configuring the variance config for pitch training 🎵

A very important DiffSinger mantra to chant for 30 minutes every night before you go to bed is this: ***NEVER TRAIN DURATION AND PITCH TOGETHER!***
TLDR: Training pitch & duration together will bottleneck each model respectively, basically capping how good they can get. You'll just have to take my word for it, the developers have also said it but I cannot find the quote :sob:

SO! We need to edit the variance configuration to give us what we need. Basically, we're going to be training a model from scratch, so we won't fine-tune, and we want to change a few other specifics. 

Below, you'll find each line that i've _changed_, but not the entire configuration. Please view the full config file [here!](https://github.com/openvpi/DiffSinger/blob/main/configs/variance.yaml) **NOTE** You can use the glide embed if you want, I currently do not so I cannot speak to how much it helps.

```yaml
predict_dur: false
predict_pitch: true
predict_energy: false
predict_breathiness: false
predict_voicing: false
predict_tension: false

use_melody_encoder: true

main_loss_type: l1

lr_scheduler_args:
  step_size: 20000

max_batch_size: 36
```

So, above you can see that the only embedding we're actually training is pitch. THIS IS **SO VERY IMPORTANT!!** Pitch will only reach the desired result when it's not bottlenecked by other embed types.

I've heard a few different things about `use_melody_encoder: true`. I personally find it helps with the pitch staying on the right note, but I've also heard others say that they have gotten good results without it. Feel free to experiment!

Now, `main_loss_type: l1` is a spicy one. From what my small, peanut sized brain understands about the difference between L1 and L2 loss, they both are good at different things. L1 loss focuses on the **absolute** difference of GT & inference, whereas L2 focuses on the **squared** difference of GT & inference.
Basically, L1 will be able to handle outliers in data much more effectively than L2, and given the fact that most people train extremely varied multispeaker datasets, L1 loss is going to be your best friend and not just on pitch. L2 would only be benificial if all data was perfectly labelled, cleaned, configured.
Admittedly, I haven't stressed tested this theory, but I don't care to and will not do it 😺.

As for LR, I personally have found that 20000 steps before lowering the LR to be a nice value. I usually train my models to 100k steps, so by the end of training the learning rate will drop 4 times by a factor of 0.75. This may not be the most ideal, but it works for me!

Batch size can be a bit tricky, it highly depends on your GPU. I train at 36 mostly because of the size of the dataset, if I was to add an hour or so to it, I would jump up to ensure my model has ample time to learn all of the data.

# Step 3: Train your model 🏃

Sounds simple enough, train your model! Again, we are NOT fine-tuning. If you fine-tune off of a model with shit pitch, it's not going to get as good as training from scratch, because you're basically telling the model to build good pitch off of shit pitch. I hope that makes sense.

Once your model is fully trained, export your model and try it out! Good luck!



