import sys
sys.path.insert(0, '/usr/lib/cas-mockup/')
sys.path.insert(1, '/usr/lib64/python3.6')

activate_this = '/usr/lib/cas-mockup/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


from app import app as application

application.debug = True
