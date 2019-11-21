from flask_cors import CORS

from goodsapp.views import goods_api
from homeapp.views import home_api
from mainapp import app
from settings import HOST, PORT
from mainapp.views import user_api
from shopapp.views import shopcar_api

app.register_blueprint(user_api.user_blue, url_prefix='/user')
<<<<<<< HEAD
app.register_blueprint(goods_api.goods_blue, url_prefix='/goods')
app.register_blueprint(home_api.home_blue, url_prefix='/home')
=======
app.register_blueprint(shopcar_api.shopcar_blue, url_prefix='/cart')
>>>>>>> 2359345aff50a115e887fdb384f369b6115068fe
CORS(app)
app.run(host=HOST, port=PORT)