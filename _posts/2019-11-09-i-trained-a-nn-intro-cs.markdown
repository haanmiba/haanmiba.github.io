---
layout: post
title: "I Trained a Neural Network to Generate Piazza Posts for an Introductory Computer Science Class"
date: 2019-11-09 01:26:00 -4000
categories: blog personal review
preview: "Because why not?"
---

### Introduction

A little background: I am an undergraduate teaching assistant for CSE 115: Introduction to Computer Science I, the introductory course for computer science majors at the University at Buffalo. The course utilizes this handy website called [Piazza](https://piazza.com/) which acts as a forum where students and instructors can ask and answer questions. As a TA, I can observe all of the posts made on Piazza by students, both public **and** private.

Now that we just finished week 11 of fall semester at UB (at the time of writing this blog post), I am beginning to notice a trend on our Piazza page. Since Piazza is the hub for all student questions, many of the posts on Piazza are aimed towards students asking for help with their code – your usual "my code isn't working!" **or** "X isn't displaying correctly" or **my** favorite: "my code is correct, I don't know what I'm doing wrong." Since I am beginning to see a pattern of these common posts, I decided to delve into the wonderful, mysterious world of neural networking to see if a neural network can see this same pattern that I am seeing.

### Neural Networks

<img src="https://miro.medium.com/proxy/1*DW0Ccmj1hZ0OvSXi7Kz5MQ.jpeg" style="max-width:100%" />

So what's a [neural network](https://en.wikipedia.org/wiki/Artificial_neural_network)? A neural network is a machine learning model that models itself after the human brain. These models "learn" to perform tasks by looking at examples. The "examples" for our purposes, will be Piazza posts from CSE 115 students.

Neural networks can be used to detect patterns and use these patterns to create new things. Some of my favorite examples of these have actually gone viral recently, like a neural network that [writes candy heart messages](https://aiweirdness.com/post/170685749687/candy-heart-messages-written-by-a-neural-network), a neural network that [generated a film](https://arstechnica.com/gaming/2018/06/this-wild-ai-generated-film-is-the-next-step-in-whole-movie-puppetry/), and my personal favorite – an AI that [wrote Harry Potter fan fiction](https://www.mentalfloss.com/article/520897/ai-program-wrote-harry-potter-fan-fiction-and-results-are-hilarious).

### Step 0: Planning and Design

So **before** we start coding, we need to think about what our program will exactly do. So let's break it down. First, let's think about our goal:

**GOAL:** Have an neural network generate Piazza posts from the CSE 115 Piazza.

Now that we have our goal, we need to break it down into actionable steps. Essentially, we have to take the goal and break it down into smaller and smaller tasks that we can logically work with in a chronological order. So let's do that. Our program must do the following (in this order):

- Connect to the Piazza API
- Fetch posts from the CSE 115 Piazza
- Store these posts in a text file
- Train an neural network from these posts in the text file
- Have the neural network generate new CSE 115 Piazza posts

### Step 1: Create the Project Directory

Since I'm a TA for CSE 115 and we're primarily working with **Python**, I'm going to be using Python to write this project. It only makes sense.

The first thing I'm going to do is create a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) for this project just so it has an isolated environment, separate from my other projects.

If you do not have Python on your local machine, download it from the [Python website](https://www.python.org/). This should come with `pip`, a package manager for Python.

If you do not have `virtualenv`, we are going to install it using `pip`:

```bash
$ pip install virtualenv
```

Next, run the following commands to create our project and its virtual environment:

```bash
# Create project directory
$ mkdir cse-115-neural-network

# Switch into project directory
$ cd cse-115-neural-network

# Create virtual environment
$ virtualenv .venv

# Activate virtual environment
$ source .venv/bin/activate
```

The next step is to create a Python file to run. I'm going to run the command below to create a Python file called `fetch_piazza_posts.py`:

```bash
$ touch fetch_piazza_posts.py
```

Next, open this directory in your favorite text editor/IDE (Visual Studio Code, PyCharm, Atom, Sublime Text) or `vim` if you're feeling fancy. The contents of `fetch_piazza_posts.py` will be the following (this will change as we add more code!)

```python
def main():
    pass

if __name__ == '__main__':
    main()
```

### Step 2: Connect to an API to access Piazza Posts

Bad news, Piazza has a private API. Good news, this wonderful person [Hamza Faran](https://hfaran.me/posts/reverse-engineering-piazzas-api/) reverse-engineered Piazza's private API and wrote a client for it on [GitHub](https://github.com/hfaran/piazza-api).

The client is a Python module that we can import. The instructions for installation and importing can be found on the [README.md](https://github.com/hfaran/piazza-api/blob/develop/README.md) on the GitHub repository. We're going to install it with `pip` (make sure your virtual environment is running! You will know if it's running if the bottommost line in your terminal starts with `(.venv)`:

```bash
(.venv)$ pip install piazza-api
```

Once this is installed, we need to actually import it in our `fetch_piazza_posts.py`:

```python
from piazza_api import Piazza

def main():
    pass

if __name__ == '__main__':
    main()
```

Then we need to use it, just to see if it works. Within our `main()` function, we are going to create an instance of `Piazza` and have the user log in:

```python
from piazza_api import Piazza

def main():
    piazza = Piazza()
    piazza.user_login()

if __name__ == '__main__':
    main()
```

Now all we need to do is run our program – it should ask you for your Piazza email and password:

```bash
(.venv)$ python fetch_piazza_posts.py
Email: <enter your email here>
Password: <enter your password here>
```

So as of right now, all our program does is connect to Piazza via this Piazza Python client and our user credentials. However one annoying step – every time we run our script with `python fetch_piazza_posts.py`, we are required to enter our email and password. This is a tiny inconvenience that adds a few seconds, but these seconds will add up over time.

My suggestion is to store our credentials in a file called `credentials.json` that will only exist locally on our machine so that when we run our script, we won't have to enter our email and password every time.

So create a file called `credentials.json` in the same directory as `fetch_piazza_posts.py`, and structure it like so:

```JavaScript
{
  "email": "<your_email_here>",
  "password": "<your_password_here>"
}
```

**_NOTE: Do not show anyone the contents of this `credentials.json` file. It is for your eyes only. This means do not push it up to GitHub or share it with a friend. Sharing the `credentials.json` file is basically giving away your Piazza credentials._**

Now we want to restructure our `fetch_piazza_posts.py` so that it reads the contents of this `credentials.json` and passes it to `piazza.user_login(...)` so that it automatically logs us in, rather than asking us. So we need a few things:

- Import `json` library
- Variables for `EMAIL`, and `PASSWORD`

```Python
import json
from piazza_api import Piazza

EMAIL = None
PASSWORD = None

with open('credentials.json') as f:
    credentials = json.load(f)
    EMAIL = credentials.get('email', None)
    PASSWORD = credentials.get('password', None)

def main():
    piazza = Piazza()
    piazza.user_login(email=EMAIL, password=PASSWORD)

if __name__ == '__main__':
    main()

```

Now if we run `python fetch_piazza_posts.py`, we shouldn't have to log in.

**Scenario: What if we don't make `credentials.json`?**

Ah! So let's say we don't have a file named `credentials.json`. This can lead to some issues, like the following:

```
FileNotFoundError: [Errno 2] No such file or directory: 'credentials.json'
```

Well our code should account for this. It would be annoying for our program to not be able to run just because the user doesn't create a `credentials.json` file. So let's add a check if the file exists. This requires us to import the `os` package and use it to check if the file exists:

```Python
import json
import os
from piazza_api import Piazza

EMAIL = None
PASSWORD = None

if os.path.exists('credentials.json'):
    with open('credentials.json') as f:
        credentials = json.load(f)
        EMAIL = credentials.get('email', None)
        PASSWORD = credentials.get('password', None)

def main():
    piazza = Piazza()
    piazza.user_login(email=EMAIL, password=PASSWORD)

if __name__ == '__main__':
    main()
```

Now we have to actually fetch the Piazza posts. This means we need to access the course using the course's network ID and a call to `piazza.network(...)`.

To get the course ID, go on a web browser and pull up the Piazza page for your class (in this case, it is CSE 115). The network ID can be found in the URL: `https://piazza.com/class/{network_id}`

So how do we get the network ID into our script? We don't want to hardcode the network ID – what if we want to use this script to fetch posts from another class's Piazza? So the best thing to do is to ask the user for their course ID with a call to `input(...)`:

```Python
import json
import os
from piazza_api import Piazza

EMAIL = None
PASSWORD = None

if os.path.exists('credentials.json'):
    with open('credentials.json') as f:
        credentials = json.load(f)
        EMAIL = credentials.get('email', None)
        PASSWORD = credentials.get('password', None)

def main():
    piazza = Piazza()
    piazza.user_login(email=EMAIL, password=PASSWORD)
    network_id = input("Input your course's Piazza network ID: ").strip()
    course = piazza.network(network_id)

if __name__ == '__main__':
    main()
```

So what comes next after this? Well we need to get all the posts from the course's Piazza page. This would be done through a call to `course.iter_all_posts()`. This method returns a generator that will fetch each post one by one. Since some course Piazza pages will have hundreds to thousands of posts, let's limit ourselves for now with a limit of `10` posts, printing each post to the console:

```Python
import json
import os
from piazza_api import Piazza

EMAIL = None
PASSWORD = None

if os.path.exists('credentials.json'):
    with open('credentials.json') as f:
        credentials = json.load(f)
        EMAIL = credentials.get('email', None)
        PASSWORD = credentials.get('password', None)

def main():
    piazza = Piazza()
    piazza.user_login(email=EMAIL, password=PASSWORD)
    network_id = input("Input your course's Piazza network ID: ").strip()
    course = piazza.network(network_id)
    posts = course.iter_all_posts(limit=10)
    for post in posts:
        print(post)

if __name__ == '__main__':
    main()
```

Now when we run `python fetch_piazza_posts.py`, we're going to see a series of ten dictionaries printed to our console, each one with this format:

```json
{
  'bookmarked': 2,
  'bucket_name': 'Pinned',
  'bucket_order': 0,
  'change_log': [{...}],
  'children': [],
  'config': {
    'bypass_email': 1,
    'is_announcement': 1
  },
  'created': '2019-11-07T20:33:26Z',
  'data': {'embed_links': [...]},
  'default_anonymity': 'no',
  'folders': ['other'],
  'history': [{...}],
  'i_edits': [],
  'id':'a0bcdejo13498fb',
  'is_bookmarked': False,
  ...
}
```

Since we only care about the **text** of the Piazza post, we only care about one field: `post[history]`. The `history` key stores the text body of the post. The `history` field is structured like so:

```json
{
  'history': [
    {
      'anon': 'no',
      'content': '<p><strong>Here is the post content</strong></p>',
      'created': '2019-11-07T20:33:26Z',
      'subject': 'SUBJECT OF THE POST',
      'uid': 'h88rqmabcdef1xs'
    }
  ],
  ...
}
```

We just need to change our `print(...)` to print just the text, which is stored under `history`, index `0`, key `content`. So this would be `post['history'][0]['content']`:

```python
import json
import os
from piazza_api import Piazza

EMAIL = None
PASSWORD = None

if os.path.exists('credentials.json'):
    with open('credentials.json') as f:
        credentials = json.load(f)
        EMAIL = credentials.get('email', None)
        PASSWORD = credentials.get('password', None)

def main():
    piazza = Piazza()
    piazza.user_login(email=EMAIL, password=PASSWORD)
    network_id = input("Input your course's Piazza network ID: ").strip()
    course = piazza.network(network_id)
    posts = course.iter_all_posts(limit=10)
    for post in posts:
        print(post['history'][0]['content'])

if __name__ == '__main__':
    main()
```

Now if you run `python fetch_piazza_posts.py`, you may notice that you are getting some weird looking formatted text printed to your console:

```
<p>Dear students,</p>
<p>As you hopefully know by now, you have to enable Duo two-factor authentication on your UB account by November 18th. Luckily, UBIT is providing a free, easy, privacy-safe solution in the form of hardware tokens. Simply bring your UBID to the third-floor Capen UBIT helpdesk and you&#39;ll get a fob you can attach to your keychain. Press the button and you generate a one-time code. Please, <em>please</em>, <strong><em>please</em></strong><em> </em>get this done before the deadline.</p>
<p>Thank you!</p>
<p>#pin</p>
<p>We have a project 1 submission target open in AutoLab.  The submission target was accidentally open earlier, and a few submissions snuck in.  To ensure that everyone gets the benefit of all the feedback available, <strong>ALL OF THESE EARLY SUBMISSIONS HAVE BEEN REMOVED, and everyone now has 5 submissions remaining.</strong></p>
...
```

_Why am I getting this?_

The only explanation: **Piazza stores the body of the text as HTML strings!** This is great, but not what we need. Since we are training a neural network purely on text, we don't want random HTML tags throwing off its learning. This means we need to clean up the data so we only get the **text** within the posts.

**How do we do this?**

Let's use a Python library! The great thing about Python is the community around it, and Python's community creates a **lot** of libraries for us to use.

Let's use a Python library called [html2text](https://github.com/aaronsw/html2text), which takes HTML and converts it to Markdown-formatted text. Let's just install it:

```bash
$ pip install html2text
```

And then use it:

```Python
import json
import os
from html2text import HTML2Text
from piazza_api import Piazza

HTML_2_TEXT = HTML2Text()
HTML_2_TEXT.ignore_links = True

EMAIL = None
PASSWORD = None

if os.path.exists('credentials.json'):
    with open('credentials.json') as f:
        credentials = json.load(f)
        EMAIL = credentials.get('email', None)
        PASSWORD = credentials.get('password', None)

def main():
    piazza = Piazza()
    piazza.user_login(email=EMAIL, password=PASSWORD)
    network_id = input("Input your course's Piazza network ID: ").strip()
    course = piazza.network(network_id)
    posts = course.iter_all_posts(limit=10)
    for post in posts:
        post_content = post['history'][0]['content']
        post_content_as_text = HTML_2_TEXT.handle(post_content)
        print(post_content_as_text)

if __name__ == '__main__':
    main()
```

Now when I run `python fetch_piazza_posts.py`, I get this printed to my console:

<pre><code class="plaintext">Dear students,

As you hopefully know by now, you have to enable Duo two-factor authentication
on your UB account by November 18th. Luckily, UBIT is providing a free, easy,
privacy-safe solution in the form of hardware tokens. Simply bring your UBID
to the third-floor Capen UBIT helpdesk and you'll get a fob you can attach to
your keychain. Press the button and you generate a one-time code. Please,
_please_ , **_please_** __ get this done before the deadline.

Thank you!

#pin




We have a project 1 submission target open in AutoLab. The submission target
was accidentally open earlier, and a few submissions snuck in. To ensure that
everyone gets the benefit of all the feedback available, **ALL OF THESE EARLY
SUBMISSIONS HAVE BEEN REMOVED, and everyone now has 5 submissions remaining.**
</code>
</pre>

So we are doing a lot better than before, but not quite. We should still clean this up, which means removing newlines, removing unnecessary whitespace, and using regex to clean up some more complex patterns (image links, etc.). So I'm going to add some more function calls to clean up Piazza post content:

```Python
import json
import re
import os
from html2text import HTML2Text
from piazza_api import Piazza

HTML_2_TEXT = HTML2Text()
HTML_2_TEXT.ignore_links = True

EMAIL = None
PASSWORD = None

if os.path.exists('credentials.json'):
    with open('credentials.json') as f:
        credentials = json.load(f)
        EMAIL = credentials.get('email', None)
        PASSWORD = credentials.get('password', None)

def main():
    piazza = Piazza()
    piazza.user_login(email=EMAIL, password=PASSWORD)
    network_id = input("Input your course's Piazza network ID: ").strip()
    course = piazza.network(network_id)
    posts = course.iter_all_posts(limit=10)
    for post in posts:
        post_content = post['history'][0]['content']
        post_content_as_text = HTML_2_TEXT.handle(post_content)
        post_content_as_text = post_content_as_text.replace('\n', ' ')
        post_content_as_text = post_content_as_text.replace('  ', ' ')
        post_content_as_text = post_content_as_text.strip()
        post_content_as_text = re.sub(r'!\[\]\(.*\)', '', post_content_as_text)
        print(post_content_as_text)

if __name__ == '__main__':
    main()
```

So now when we run `python fetch_text_posts.py`, we get this printed to console, which is super clean!

<pre><code class="plaintext">Dear students, As you hopefully know by now, you have to enable Duo two-factor authentication on your UB account by November 18th. Luckily, UBIT is providing a free, easy, privacy-safe solution in the form of hardware tokens. Simply bring your UBID to the third-floor Capen UBIT helpdesk and you'll get a fob you can attach to your keychain. Press the button and you generate a one-time code. Please, _please_ , **_please_** __ get this done before the deadline. Thank you! #pin
We have a project 1 submission target open in AutoLab. The submission target was accidentally open earlier, and a few submissions snuck in. To ensure that everyone gets the benefit of all the feedback available, **ALL OF THESE EARLY SUBMISSIONS HAVE BEEN REMOVED, and everyone now has 5 submissions remaining.** Before submitting, be sure to review the submission requirements. I have tested the submission target but will monitor throughout the weekend in case there are any issues. As noted in @410, we have pushed the submission deadline to Friday, November 8 @ 5:00 PM. #pin
</code></pre>

Final thing, now let's change our code so that instead of printing to console, we write this to a file. Let's change a few things:

- Prompt user to name the file where these Piazza posts will be output to
- Remove `limit` from `course.iter_all_posts(...)`
- Write to a file using `f.write(...)`

```Python
import json
import re
import os
from html2text import HTML2Text
from piazza_api import Piazza

HTML_2_TEXT = HTML2Text()
HTML_2_TEXT.ignore_links = True

EMAIL = None
PASSWORD = None

if os.path.exists('credentials.json'):
    with open('credentials.json') as f:
        credentials = json.load(f)
        EMAIL = credentials.get('email', None)
        PASSWORD = credentials.get('password', None)

def main():
    piazza = Piazza()
    piazza.user_login(email=EMAIL, password=PASSWORD)
    network_id = input("Input your course's Piazza network ID: ").strip()
    course = piazza.network(network_id)
    posts = course.iter_all_posts()
    filename = input("What is the name of the file you want to write these Piazza posts to? ").strip()
    with open(filename, 'w') as f:
        for post in posts:
            post_content = post['history'][0]['content']
            post_content_as_text = HTML_2_TEXT.handle(post_content)
            post_content_as_text = post_content_as_text.replace('\n', ' ')
            post_content_as_text = post_content_as_text.replace('  ', ' ')
            post_content_as_text = post_content_as_text.strip()
            post_content_as_text = re.sub(r'!\[\]\(.*\)', '', post_content_as_text)
            f.write(post_content_as_text + '\n')

if __name__ == '__main__':
    main()
```

So now when we run `python fetch_piazza_posts.py`, we get the following prompt:

```
Input your course's Piazza network ID: <insert network ID here>
What is the name of the file you want to write these Piazza posts to? <filename.txt>
```

And the `<filename>.txt` should contain all the plain text Piazza posts, each post getting its own line!

### Step 3: Training the Neural Network to Generate Text

**Fun fact:** training the neural network to generate text was the easiest part of this whole process.

We will be using [textgenrnn](https://github.com/minimaxir/textgenrnn), a Python module on top of [TensorFlow](https://www.tensorflow.org/).

First we have to install `tensorflow` since that is what `textgenrnn` needs to run, then we will install `textgenrnn`:

```bash
(.venv)$ pip install tensorflow
(.venv)$ pip install textgenrnn
```

Then all we need is to create a `textgenrnn` model to train. We don't even need a Python file for this, we're going to do this directly from the Python REPL. So launch a Python REPL:

```bash
(.venv)$ python
```

And now we are in the REPL. Let's begin playing around with `textgenrnn`:

```Python
>>> from textgenrnn import textgenrnn
>>> textgen = textgenrnn()
```

And let's train it using the file with all our Piazza posts stored as text. Just so we can train our model a bit but not have to wait too long, let's use `3` epochs for training:

```Python
>>> textgen.train_from_file('<filename>.txt', num_epochs=3)
```

You may notice that there is a new file in your directory called `textgenrnn_weights.hdf5`. This file simply stores the model weights. This means if you ever want to work with this model again, you don't need to retrain it, you can just reconstruct it using this file:

```Python
>>> textgen_2 = textgenrnn('textgenrnn_weights.hdf5')
```

Last step: generating posts. The first argument is the number of posts to generate, the second argument (`temperature`) is how "creative" the model is when generating posts (0.0 means less creative, 1.0 means more creative). I personally like to generate with `temperature=0.2` or `temperature=0.5`. But do whatever you wish.

**_Note: near temperature=1.0 you may start to get gibberish._**

```Python
>>> textgen_2.generate(3, temperature=0.5)
```

<pre><code class="plaintext">I submitted my code when I submitted this.

I cannot find appcode.py file in the first event.

I have to do this study of the second floor lounge and help?
</code></pre>

If you want to save your model's generated text, just do the following (tweaking arguments to your liking – `n` is the number of posts to generate, `temperature` is how creative the neural network should be):

```Python
>>> textgen_2.generate_to_file('file_to_write_to.txt', n=10, temperature=0.5)
```

And now we have trained an neural network to generate CSE 115 Piazza posts! The section below details some of my favorite texts that it has generated:

### Some of my favorite outcomes from generating CSE 115 Piazza text posts

_I have to find the file of the code of the function is not sure what to see it in the code to get the project of the function in the file in the project for the file in the function in the function in the function filterByMonth failed._

_I have sure what to receive the project and the look in the project and the function in the function in the function in the function in the function filterByMonth(lines)_

_Hello, I was bottled to be in the study?_

_I have string the section of representing the input is an event but I don't understand what is my own code when there is an error to a research study?_

_I was working on the project and I was working on the project and every time I have to fix this._

_I am not sure why this is not wanted to be anything I'm not sure why this is a problem. I'm not sure why this is when I cancelled the route is a point and go to_

_How do I fix this question._

_I am unsure of what to figure out I can't figure out my code and the function is a list of the project of the first time submission cannot submit._

_I am not sure where to fix this?_

_Hey to return a function that is not a function in the project and request to participate in the server or when I submit it is wrong?_

_I am having trouble file and the project running tests. I can't figure out what I am getting._

_Hello, I submitted my code with this error on whose I'm doing wrong._

_I'm doing wrong._

_Hi everyone, Sorry for this problem._

_I have to fix this. I'm not sure whats welped._

_I cannot find this._

_I am doing wrong from the list to the beginning. I am not sure why what I'm doing wrong with the graphs that I submitted to expected out in the graphs._

_I cannot fix this issue is being complete the same as the semester, please help._

_I cannot find appcode.py file in the first event._

_I have been wrong._

_I am getting this code and why is that if you have to fix this problem._

_I cannot figure out what I'm doing wrong._

_I am still working on my code because I cannot find this problem and some help?_

_How do I see how to fix this._

_I am not sure why this is what I'm doing wrong._

_I submitted my code when I submitted this._

_How do I check you! I have to filter the distance of the same project or we submit it and then it would be able to get the dictionaries?_

_I was still working on the data file and it doesn't work._

### Conclusion

As you can see, the neural network can _kinda_ make some coherent sentences that resemble CSE 115 Piazza posts – mainly students asking for help and not knowing what their code is doing. I trained it on my own on approximately 12 epochs (this took almost 2 hours), so I'm sure if I trained it much longer, it would create much better sentences.

**DISCLAIMER: You will not get quality generated text 100% of the time.** The generated sentences I have above are just curated outcomes from hundreds of sentences the neural network has generated. Most of the sentences that the neural network generates are not coherent or not even that funny, I only saved the ones I liked. The reason why the viral neural network generated [candy heart messages](https://aiweirdness.com/post/170685749687/candy-heart-messages-written-by-a-neural-network) and [Harry Potter fanfiction](https://www.mentalfloss.com/article/520897/ai-program-wrote-harry-potter-fan-fiction-and-results-are-hilarious) are so great is because these were curated/edited from tons of generated text.

**Have fun with your new Piazza neural network!**
