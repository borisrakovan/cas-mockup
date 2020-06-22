import sys

sys.path.insert(0, '/usr/lib64/python3.6/hashlib.py')
sys.path.append('/usr/lib/cas-mockup/')
print(sys.path)


activate_this = '/usr/lib/cas-mockup/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


from app import app as application

application.debug = True
