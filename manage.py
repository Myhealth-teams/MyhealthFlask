from flask_cors import CORS

from mainapp import app
from settings import HOST, PORT
from mainapp.views import user_api
from shopapp.views import shopcar_api

app.register_blueprint(user_api.user_blue, url_prefix='/user')
app.register_blueprint(shopcar_api.shopcar_blue, url_prefix='/cart')
CORS(app)
app.run(host=HOST, port=PORT)