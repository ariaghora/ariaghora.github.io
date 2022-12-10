# Deep learning is not really the future of AI

Deep learning is often mentioned as if it is the future of AI, and is even sometimes placed as the definition of AI. However, this is not accurate. AI is not deep learning; deep learning is a special case of neural networks, which is just one of the many machine learning models available. Machine learning itself is just a branch of AI.

So, what is the "future" that we expect? Let's say we imagine a future where there are robots and humanoids with human-level intelligence. I am not even sure that we have settled on a definition of "intelligence," and I will not delve too much into this philosophical aspect of AI. But let's just say that human-level means that the agents with AI can solve general tasks and make decisions just like humans. Can deep learning achieve that?

For the current state of deep learning, the answer is no. What do we have now? We have a model that can "learn" from data. We can view the model as a machine with a bunch of configurations and internal states. The machine can accept inputs, process them, and spit out an answer. For example, when we give a picture of a cat, it will say "it is a cat!" We typically provide it with a bunch of examples to learn from: input samples and the corresponding (assumed-to-be) correct answers. The model aims to find the best configuration to make a prediction based on an input that is as close as possible to the correct answer.

Initially, we start with a stupid model: it will produce garbage predictions. Fortunately, we also provide the correct answers, so the model knows *how wrong its predictions are* compared to the actual answers. The prediction quality is measured by some "stupidity score." The score is high in the beginning, meaning the model is still dumb and its configurations are purely randomized. Based on that stupidity score, the model then updates its internal configuration such that the predictions in the next iterations can be better. In other words, the stupidity score gets lower the more the model makes predictions and updates its configuration iteratively. Finally, after we are confident enough with the model, let's expect the model can perform well on unseen data in the wild.

# Inability to explain its own decision

If you have ever watched Psycho-Pass anime (No? What are you doing? Go watch it!) you will see an example an idealized AI-assisted law enforcement system. A group of police officers are equipped with an AI-powered gun, called [the dominator](https://psychopass.fandom.com/wiki/The_Dominator).

> When the Dominator is aimed at a target, it continuously reads and sends psychological data ‒ the individual's [Psycho-Pass](https://psychopass.fandom.com/wiki/Psycho-Pass) ‒ which it sends to the Sibyl System for calculation of their [Crime Coefficient](https://psychopass.fandom.com/wiki/Crime_Coefficient_(Index)). When this value exceeds a certain level, one indicating that the target is mentally unstable and likely to commit a violent crime, the gun will be operable. If the level does not exceed such levels, the muzzle will not open and a safety device will be activated to prevent the user from pulling the gun's trigger. ...

Simply put, the officers rely on AI to determine the crime level of a suspect. The higher the level, the more lethal the bullet is. The prediction is highly accurate and they seem to trust it. Pretty neat, isn't it?

![Psycho-Pass Wallpapers - Wallpaper Cave](https://wallpapercave.com/wp/wp1874877.jpg)

Is there any chance of adopting such AI-assisted decision making with current state of deep learning? It is not difficult to sense physiological sensor of a person and fit a prediction model of the crime level. In fact, researchers are actually using physiological data [for](https://www.sciencedirect.com/science/article/pii/S157106611930009X) [many](https://ieeexplore.ieee.org/abstract/document/6681508) [purposes](https://ieeexplore.ieee.org/abstract/document/9094297/). It is one thing. The problem is that the existing deep learning models are *bad at explaining their own decision*.

In the implementation, a deep learning model works by applying a sequence of transformations (convolutions, matrix multiplications, and other arithmetical operations) on the input data to get the predicted output. A deep learning model may contain a thousands-to-billions of individual numbers. The transformations are parameterized by those numbers. Unfortunately, we cannot directly interpret them. Neither can the model. What we can rely for now is the low stupidity score of the model, which doesn't say much about the reasoning behind the decision. The score only tells us about how good the model predict the previous data.

I doubt we can expect anything from an AI that cannot explain its own decision. Especially, if we are talking about people's life. Imagine if an AI judge in a court accuse you as a level-5 criminal, and when you ask why, it says, "I don't know why. What I know is that I am good enough in predicting previous people's crime levels. Thus, you should trust me."

# Very specific to one ore few tasks

By current learning scheme, we will only get a very specific model. When we train a model to recognize objects based on images, it will solely work on that object recognition task. It is pretty much useless when we feed it emails in our inbox and ask it to distinguish which ones are spam and which ones aren't.

I understand that there is a model variant called *multi-task learning*, which aims to solve several tasks using a single model. [Self-driving cars](https://blogs.nvidia.com/blog/2019/04/15/how-does-a-self-driving-car-see/) use this type of model to detect, for example, moving objects, road signs, and traffic light color, at the same time using the same model. It can accept multiple types of input. However, the tasks should be closely related. Self-driving car AI can only work with driving and traffic related tasks. It will have a hard time predicting weather in next few hours and future stock market prices.

# But it is still useful

Despite of the limitation at current stage, in practice, deep learning still works incredibly well to solve the problems in several domains. To name few:

- Language translation. We use google translate often.
- Movie recommendation system. I don't know about you, but Netflix did the job well for me.
- Self-driving cars. Tesla, Hyundai. It goes to production now. I still have trouble to put my trust in them, though.
- Image enhancement. I use [remini](https://www.bigwinepot.com/index_en.html) quite a lot to restore old photos of my family.

Nonetheless, if you think these kind of technology is the future that you are talking about, then the future is now. The journey still continues.