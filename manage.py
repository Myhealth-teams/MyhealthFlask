from doctorapp.views import doctor_api
from flask_cors import CORS

from forumapp.views import forum_api
from goodsapp.views import goods_api
from homeapp.views import home_api
from mainapp import app
from settings import HOST, PORT
from mainapp.views import user_api
from shopapp.views import shopcar_api


def make_app():
    app.register_blueprint(user_api.user_blue, url_prefix='/user')
    app.register_blueprint(goods_api.goods_blue, url_prefix='/goods')
    app.register_blueprint(home_api.home_blue, url_prefix='/home')
    app.register_blueprint(shopcar_api.shopcar_blue, url_prefix='/cart')
    app.register_blueprint(doctor_api.doctors_blue, url_prefix='/doctor')
    app.register_blueprint(forum_api.forum_blue, url_prefix='/forum')
    CORS(app)
    return app


application = make_app()
if __name__ == '__main__':
    application.run(host=HOST, port=PORT)
