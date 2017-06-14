Title: Getting started with Hu:toma.ai chat bot platform
Date: 2017-05-13 10:20
Category: Articles
Status: draft

[Hu:toma](https://www.hutoma.com/) recently launched their open beta, and since I've had 
a bit of fun playing around with it, I think it deserves a quick post. So what is Hu:toma?
It's a platform for developing, publishing and selling conversational bots. It enables developing 
and training bots that your users can have a free-text conversation, while integrating with your 
APIs. For example:

![Pizza ordering through a free-text chat]({filename}/images/pizza-chat.png)

Hu:toma lets developers upload some training data in the form of example conversations. 
It then trains the bot using their deep learning network to allow the bots to understand 
variations of the questions and requests from the users. For more info, watch this [95 second video](https://www.youtube.com/watch?v=fB82FyKD674) or check out their [site](https://www.hutoma.com/).

Getting started
---------------

Before you can build your first bot, you need to get access to the beta program. At the time of 
writing there was a wait list for the beta, but this might change soon. To join the waitlist,
hit their page and click Login, it'll ask for your email. Once you receive the invite, you can
start training your chat-bot army. 

Once that's sorted, you can log in to the (console)[https://console.hutoma.com] and create your 
first bot. Hit the green `Create Bot` button:

![Hutoma 1]({filename}/images/hutoma1.png)

Name it something appropriate, I started off with the familiar name of `Hello World Bot`, some description, and leaving the other options unchanged:

![Hutoma 2]({filename}/images/hutoma2.png)

Hit `Next`, then save your creation:

![Hutoma 3]({filename}/images/hutoma3.png)

Next step is to prepare some basic conversation samples to let the neural net train the bot. Start
with something basic, and create a text file with these lines:

```
hi
hello, world!

who are you?
I am the Hello World bot

what is your purpose?
I pass the butter.
```

In the console, hit `select txt file`, pick your newly created training data and upload it:

![Hutoma 4]({filename}/images/hutoma4.png)

After the upload, the training process will start. Once it finishes, you can try chatting to your
newly trained bot. Note how you do not have to use the exact phrases from training data. For example,the bot will match both `hi` and `hello` to the response associated with `hi`:

![Hutoma 5]({filename}/images/hutoma5.png)
