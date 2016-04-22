# What is tychedice?

Tychedice is a simple Hipchat integration.

Simply run this somewhere hipchat can reach, Then add an integration. Use the slash command "roll" and post to your http://public-url.com/roll


#How do I get tychedice up and running locally?

``` bash
git clone https://github.com/CityGenerator/tychedice.git
cd tychedice
virtualenv env
source env/bin/activate
pip install -r requirements
nosetests
./run.py

```

#How do I get it up and running publicly?

Your best bet is to use supervisord and gunicorn, however I'm too tired to really document that right now.

#What does it look like?

![Example Rolls](/example/example_rolls.png)

