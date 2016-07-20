# start the application after importing all relative app components
from app import app
app.run(host='0.0.0.0', port=app.config['PORT'], debug=app.config['DEBUG'])
