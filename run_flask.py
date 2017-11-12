import os

from subprocess import Popen

os.environ["FLASK_APP"] = "service/server.py"
flask_ps = Popen(["flask", "run", "--host=0.0.0.0"])
flask_ps.communicate()
