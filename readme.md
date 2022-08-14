The final for CWK level 7

You pretty much just had to do the server side of a login system.

I decided to mess around with argon2 also so the passwords should be reasonably secure. The app should hopefully be sql injection resistant too thanks to sqlalchemy.

I lost access to my heroku account so I couldn't setup a mysql server or publish it there. I'll add a link to this readme when I get access to my account again and publish it.

#### Installation

```bash
# Make a virtualenv
pyrhon3 -m venv venv

# Activate the virtualenv
source venv/bin/activate
# Windows:
# .\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run the server
python main.py
```