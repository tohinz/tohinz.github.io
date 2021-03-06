---
layout: blog
title: Improved Techniques for Training Single-Image GANs
author: Tobias Hinz
date: 2020-03-24
description: Overview of our paper about training GANs on a single image for tasks such as image generation, image harmonization, and image animation.
thumbnail: /images/publication/thumbnails/consingan.jpg
mathjax: true
comments: true
---

Recently there has been an interest in the potential of learning generative models from a single image, as opposed to from a large dataset. This task is of practical significance, as it means that generative models can be used in domains where collecting a large dataset is not feasible. Fig. 1 shows an example of what a model trained on only a *single* image can generate.

<figure><center><img src="/images/blog/ConSinGAN/examples/unconditional-generation.jpg" alt="Unconditional Image Generation" width="50%"/><figcaption>Fig. 1: Examples of our model trained on a single image for unconditional image generation.</figcaption></center></figure>

Single-image generative models can also be used for many other tasks such as image super-resolution, image animation, and image dehazing. Fig. 2 and Fig. 3 show some examples of our model applied to image harmonization and image editing.

<figure><center><img src="/images/blog/ConSinGAN/examples/harmonization_1.jpg" alt="Image Harmonization" width="40%"/><figcaption>Fig. 2: Examples of our model applied to image harmonization.</figcaption></center></figure>

<figure><center><img src="/images/blog/ConSinGAN/examples/editing.jpg" alt="Image Editing" width="40%"/><figcaption>Fig. 3: Examples of our model applied to image editing.</figcaption></center></figure>

You can even use them for tasks such as image animation as seen in Fig. 4.

<figure><center><img src="/images/blog/ConSinGAN/examples/animation_bush.gif" alt="Image Animation" width="35.5%"/><img src="/images/blog/ConSinGAN/examples/animation_lightning.gif" alt="Image Animation" width="40%"/><figcaption>Fig. 4: Examples of image animation. The first and third images show animation with strong effects, while the second and fourth images show animation with weaker effects.</figcaption></center></figure>

The first work that introduced GANs for unconditional image generation trained on a *single natural* image was [SinGAN](https://arxiv.org/abs/1905.01164){:target="_blank"}, presented at ICCV 2019. Before that, several other approaches trained GANs on single images, however, these images where either not *natural* images (e.g. [these](https://link.springer.com/chapter/10.1007/978-3-319-46487-9_43){:target="_blank"} [approaches](https://arxiv.org/abs/1705.06566){:target="_blank"} [for](https://arxiv.org/abs/1805.04487){:target="_blank"} texture synthesis) or the task was not to learn an unconditional model (e.g. [InGAN](https://arxiv.org/abs/1812.00231){:target="_blank"} for image retargeting). This blog post summarizes our paper [Improved Techniques for Training Single-Image GANs](https://www.google.com){:target="_blank"} in which we look into several mechanisms that improve the training and generation capabilities of GANs on single images. 

Our main contributions, which we will summarize in the following post, are:  

- training architecture and optimization: we identify several aspects of the architecture and optimization process that are critical to the success of training Single-Image GANs;
- rescaling approach for multi-stage training on different resolutions: the approach to rescale images for the different training stages directly affects the number of stages we need to train on;
- fine-tuning approach for several tasks: we introduce a fine-tuning step on pre-trained models to obtain even better results on tasks such as image harmonization.

In the following, we will talk about each of these points in a bit more detail, before showing some of our results.

### Training Architecture and Optimization

To put our approach into perspective we quickly describe SinGAN's training procedure, before giving a more detailed overview of our approach. SinGAN trains several individual generator networks on images of increasing resolutions. Here, the first generator - working on the smallest image resolution - is the only unconditional generator that generates a image from random noise (see Fig. 5 for a visualization).

<figure><center><img src="/images/blog/ConSinGAN/models/singan/singan0.jpg" alt="SinGAN Model" width="30%"/><figcaption>Fig. 5: Training of the first generator in the SinGAN.</figcaption></center></figure>

The important part is that the discriminator is a patch discriminator, i.e. the discriminator never sees the image as a whole, but only parts of it. Through this it learns what "real" image patches look like. Since the discriminator never sees the image as a whole the generator can fool it by generating images that are different from the training image on a global perspective, but similar when looking only at patch statistics.

The generators working on higher resolutions take the image generated by the previous generator as input and generate an image of the current (higher) resolution from it. All generators are trained in isolation, meaning all previous generators' weights are kept frozen when training the current generator. Fig. 6 shows a visualization of how the training proceeds throughout the different resolutions.

<figure><center><img src="/images/blog/ConSinGAN/models/singan/singan1.jpg" alt="SinGAN Model" width="50%"/><figcaption>Fig. 6: Progress of SinGAN training throughout the different resolutions. Notice how only one generator is trained at a given time, while all others are frozen.</figcaption></center></figure>

During our experiments we observe that training only one generator at a given time, as well as propagating images instead of feature maps from one generator to the next, limits the interactions between the generators. As a consequence, we train our generators end-to-end, i.e. we train more than one generator at a given time, and each generator takes as input the features (instead of images) generated by the previous generator. Since we train several generators concurrently, we call our model the *Concurrent-Single-Image-GAN" (ConSinGAN). See Fig. 7 for a visualization.

<figure><center><img src="/images/blog/ConSinGAN/models/consingan/consingan.jpg" alt="ConSinGAN Model" width="50%"/><figcaption>Fig. 7: Progress of ConSinGAN training throughout the different resolutions. Notice how we do not train only one generator and how each generator gets the features generated by the previous generator as input (instead of images as in SinGAN).</figcaption></center></figure>

Now, the problem with training all generators is that this quickly leads to overfitting. This means that the final model does not generate any "new" images, but instead only generates the training image, which is obviously not what we want. We introduce two ways of how to prevent this from happening:

1. only train *some* of the generators at any given time, not *all* of them and
2. use different learning rates for the different generators, with smaller learning rates for earlier generators when training a given generator.

Fig. 8 visualizes our model with these two approaches implemented. As a default, we train up to three generators concurrently and scale the learning rate by 1/10 and 1/100 respectively for the lower generators.

<figure><center><img src="/images/blog/ConSinGAN/models/training/consingan.jpg" alt="ConSinGAN Training" width="50%"/><figcaption>Fig. 8: Training of a ConSinGAN on six stages. In our default setting we train up to three generatos concurrently and scale the learning rates of lower generators by factors 1/10 and 1/100 respectively.</figcaption></center></figure>

One interesting aspect of this approach is that we are now able to trade-off image diversity for fidelity by changing, e.g., the way of how we scale the learning rate for lower generators. Using a larger learning rate for the lower generators means that the generated images will, on average, be more similar to the training image. Using smaller learning rates for the lower generators, on the other hand, means that we will have more diversity (of possibly worse quality) in the generated images. Fig. 9 shows an example of what this might look like and we can see that larger learning rates of lower generators results in better image fidelity but less image diversity.

<figure><center><img src="/images/blog/ConSinGAN/models/training/lr_scale.jpg" alt="ConSinGAN Learning Rate Scaling" width="60%"/><figcaption>Fig. 9: Effects of different learning rate scalings on training. The top row shows images generated by a model where the learning rates of the lower generators were scaled by 1/10 and 1/100 respectively. The bottorm row shows results from a model where the learning rates were scaled by 1/2 and 1/4 respectively.</figcaption></center></figure>

### Improved Rescaling

While training the GAN on several stages of different resolutions seems to be a good way of training a GAN on a single image, the question is how many stages we need to train on until we can generate good images. The original SinGAN model, on average, needs to train on 8-10 individual stages. This obviously increases both the number of parameters in the model and the training time.

SinGAN originally rescales images by multiplying the image resolution of the final generator $G_N$ (e.g. 250x250 px) with a scaling factor $r$ for each stage. This means that for a given stage $n$, the image resolution that is used to train it is: 
\begin{equation}
    x_n = x_N\times r^{N-n},
\end{equation}
where $r=0.75$ is used as default value for the scaling factor and $x_N$ is the image resolution used for the final generator. 

We can downsample the images more aggressively to train the model on fewer stages, e.g. by using $r=0.55$. However, if we do this with the original rescaling approach the generated images lose much of their global coherence.

We observe that this is the case when there are not enough stages at low resolution (roughly fewer than 60 pixels at the longer side). Consequently, to achieve image consistency we need a certain number of stages (usually at least three) at low resolution. However, we observe that we do not need many stages a high resolution. Based on this observation we adapt the rescaling to not be strictly geometric (i.e. $x_n = x_N\times r^{N-n}$), but instead to keep the density of low-resolution stages higher than the density of high-resolution stages:
<span style="display: block;overflow-x: auto !important;">\begin{equation}
    x_n = x_N\times r^{((N-1)/\textit{log}(N))*\textit{log}(N-n)+1}\ \text{for}\ n=0, ..., N-1.
\end{equation}

For example, for an image $x_N$ of resolution 188x250 px using the new and old rescaling approaches leads to the following resolutions:
<span style="display: block;overflow-x: scroll !important;">\begin{aligned}
10&\text{ Stages - Old Rescaling: }\mkern-38mu &&25\times34, 32\times42, 40\times53, 49\times66,\ \ 62\times82, \ \ \ \ 77\times102, 96\times128, 121\times160, 151\times200, 188\times250 \\\ 
10&\text{ Stages - New Rescaling: }\mkern-38mu &&25\times34, 28\times37, 31\times41, 35\times47,\ \ 41\times54,\ \ \\ \ 49\times65,\ \ 62\times82,\ \ \ \ 86\times114, 151\times200, 188\times250 \\\
6&\text{ Stages - Old Rescaling: }\mkern-38mu &&25\times34, 38\times50, 57\times75, 84\times112,126\times167,188\times250 \\\ 
6&\text{ Stages - New Rescaling: }\mkern-38mu &&25\times34, 32\times42, 42\times56, 63\times84, \ \ 126\times167, 188\times250
\end{aligned}

We can see that, compared to the original rescaling method, we have more stages that are trained on smaller resolutions, but fewer stages that are trained on higher resolutions. Using this approach we can train our model on six stages and still generate images of the same quality as models trained on 10 stages with the old rescaling method.

<figure><center><img src="/images/blog/ConSinGAN/models/training/rescaling.jpg" alt="ConSinGAN Learning Rate Scaling" width="50%"/><figcaption>Fig. 10: Comparison of the old and new rescaling method when training the ConSinGAN on various stages.</figcaption></center></figure>

### Fine-tuning for Image Harmonization

Finally, since our model can be trained end-to-end we introduce a novel fine-tuning step for tasks such as image harmonization. Image harmonization is the task were you have a given image of a given style (e.g. a painting) and you want to add an object to that image that should adhere to the overall image style. For this, we first train our model on the training image as described previously. Once the model is fully trained we can additionally train it on the given "naive" image to achieve even better results. Fig. 11 shows an example of this.

<figure><center><img src="/images/blog/ConSinGAN/models/training/fine-tuning.jpg" alt="ConSinGAN Fine-tuning" width="50%"/><figcaption>Fig. 11: Fine-tuning on a given image for, e.g., image harmonization can further improve the results.</figcaption></center></figure>

### Results

We now show a small sample of our results. For more results, comparisons to SinGAN, and details please refer to our [paper and supplementary material](https://arxiv.org/abs/2003.11512){:target="_blank"} or try it for yourself with the [code we provide](https://github.com/tohinz/ConSinGAN){:target="_blank"}.

<figure><center><img src="/images/blog/ConSinGAN/examples/unconditional-generation_2.jpg" alt="Unconditional Image Generation" width="50%"/><figcaption>Fig. 12: Examples of our model for unconditional image generation.</figcaption></center></figure>

<figure><center><img src="/images/blog/ConSinGAN/examples/harmonization_2.jpg" alt="Image Harmonization" width="50%"/><figcaption>Fig. 13: Examples of our model for image harmonization.</figcaption></center></figure>



---
---

