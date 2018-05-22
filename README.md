# Voice Assistant
*Voice assistant* is a Python library to write a voice assistant.


This library is just an abstraction to build easily a voice assistant. It uses Google voice API so in this moments it
only works with an Internet connection. Also remember to have a microphone and speakers or headphones connected to the computer before
using it.


### Basic assistant example ("hello world"):

```python3
from voice_assistant import Assistant

assistant = Assistant()

while True:
    assistant.speak('What do you need?')
    assistant.listen()

    if assistant.has_heard(['hello', 'Hello', 'Good morning']):
        assistant.speak("Hello!, I'm ready for what you need.")
```


### Requirements and installation:
Before installing python dependencies, it's necessary to install system dependencies.

##### System requirements

###### Ubuntu/Debian users:

`sudo apt-get install python3 python3-pip python3-pyaudio portaudio19-dev sox libsox-fmt-mp3 python-dev build-essential swig libpulse-dev`


##### Python requirements

To install Python requirements just type:

```
pip install -r requirements.txt
```

*Note: we highly recommend to use a *virtualenv**

If you get an error trying to install Python dependencies, maybe you need to install some of this system dependencies: 
`libffi-dev libxml2-dev libxslt1-dev libpq-dev libldap2-dev libsasl2-dev libssl-dev zlib1g-dev`.

Try to install them with `sudo apt-get install <dependece>` and then try to install Python dependencies again with: `pip3 install -r requirements.txt`.


### How to use

##### Creating assistant

Just type:

```python3
from voice_assistant import Assistant

assistant = Assistant()
```

Default language is English. To use with another language you can instantiate it in this way:

```python3
assistant = Assistant(language='es')
```

*Note: Don't worry if you see messages in the standard output when you instantiate an assistant. They won't be in future versions.*


##### Speaking
Now you can make it to speak:


```python3
assistant.speak('hello')
```

You should listen "hello".

If you need to make it speak in another language just add a `language` parameter:

```python3
assistant.speak('¿Cómo estas?', language='es')
```


##### Listening

You can make the assistant to listen. To do it just type:

```python3
assistant.listen()
```

Assistant will be listening and waiting to hear something. Of course, it's necessary to have a working microphone
connected to the computer. When you stop speaking assistant stop listening and prints in the terminal what it thinks you
have said.

Of course is not the same trying to understand something if you expect to listen something in another language. So
take in mind that by default assistant is trying to listen something in the same language that it speaks. However, you
can also make it listen in another language just using the same approach than when you change its spoken language:

```python3
assistant.listen(language='es')
```

*Note: When an assistant is initialized it listen ambient noise to know how loud it should listen, so if ambient noise
changes a lot maybe you should initialize it again or use `adjust_for_ambient_noise()` method.*


You can get the last listened string calling `last_recognised` property:


```python3
assistant.last_recognised
'hello'
```

But the most powerful way to use it is just typing:


```python3
assistant.has_heard('hello')
True
```

This method returns `True` or `False` depending if word is in last recognised sentence or not.
 
The method `has_heard` can accept a word, but also accepts a list of words. If one of provided words is in the last recognised sentece, it will return `True`:

```python3
assistant.has_heard(['goodbye', 'kiss', 'hello'])
True
```


##### Sentences log
Assistant have a log of all listened sentences (in this moments it creates a simple SQLite database where is used).

To print all listened sentences just type:

```python3
assistant.get_all_listened_words()
['hello', 'how are you']
```

If you want to make it forget all listened words you can do it using:

```python3
assistant.forget_listened_words()
```

Now `get_all_listened_words()` should return an empty list.

The `last_recognised` property doesn't access to memory, it just show what it's in RAM. To get last recognised from database, you can use the `get_last_recognised_from_memory()` method.

### Memory

Sometimes it could be interesting to make the assistant to memorize a specific thing. You can do it using `memorize(keyword, value)` method, providing a keyword and a value for that keyword:

```python3
assistant.memorize('name', 'Megara')
```

Now if you want to retrieve that value you can use `remember(keyword)` method:

```python3
assistant.remember('name')
['Megara']
```

Notice that result is a list of strings and not just a string. That's because it can memorize lots of different 'concepts' with the same 'keyword'.

```python3
assistant.memorize('name', 'Pilar')

assistant.remember('name')
['Megara', 'Pilar']
```

To retrieve just the last record you can use `remember_last(keyword)`:

```python3
assistant.remember_last('name')
'Pilar'
```

Take in mind that if the keyword provided doesn't exists `remember(keyword)` will return an empty list and `remember_last(word)` an empty string.   

*Note: All thing are registered as strings. So if you want to remember a number and then use it, don't forget to cast it. Example: `years = int(a.remember_last('years'))`.*


##### Multiple assistants

There is no problem to create multiple assistants and use them at the same time, just remember that they probably won't be able to use the microphone and speakers at the same moment.

However, it's interesting to maintain they "memory" separated to discern between what an assistant has listened and what have the other listened or to separate what one knows and what the other knows. To achieve this you can just initialize them with different database_names:


```python3
from voice_assistant import Assistant

assistant = Assistant()

second_assistant = Assistant(database_name='second_memory')
```

Default database name is 'memory', so don't repeat it or specify a different database name for each assistant.

It is also possible to use the same database and just change an specific table name.

To do it you can type:
 

```python3
another_assistant = Assistant(memory_table='new_memory', listen_log_table='new_listen_log')
```

Default `memory_table` value `'memory'` and default `listen_log_table` values is `'listen_log'`.


Note: In this moment, when there is a Database error, it raises "DatabaseException". You can manage them importing it in this way: `from voice_assistant import DatabaseException`.

