
###############################
##### To fire-up the app ######
#####run this file run.py######
###############################

from Quiz_app import app
from flask_wtf.csrf import CSRFProtect
from instance import create_db 


CSRFProtect(app)

if __name__ == '__main__':
  app.run(debug=True)
