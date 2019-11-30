# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Authdeatil(Base):
    __tablename__ = 'authdeatil'

    detail_id = Column(Integer, primary_key=True)
    auth_deatil1 = Column(String(50))
    auth_detail = Column(String(50))
    auth_id = Column(Integer)


class Cart(Base):
    __tablename__ = 'carts'

    c_id = Column(Integer, primary_key=True, unique=True)
    u_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    goods_id = Column(ForeignKey('goods.goods_id'), nullable=False, index=True)
    c_goods_num = Column(Integer, nullable=False)
    c_is_selected = Column(Integer, nullable=False)

    goods = relationship('Good', lazy="immediate", primaryjoin='Cart.goods_id == Good.goods_id', backref='carts')
    u = relationship('User', primaryjoin='Cart.u_id == User.id', backref='carts')


class City(Base):
    __tablename__ = 'city'

    cityid = Column(Integer, primary_key=True, unique=True)
    provinceid = Column(Integer, nullable=False)
    cityname = Column(String(45), nullable=False)


class DiscountGood(Base):
    __tablename__ = 'discount_goods'

    dg_id = Column(Integer, primary_key=True, unique=True)
    goods_id = Column(ForeignKey('goods.goods_id'), nullable=False, index=True)
    discount = Column(Float, nullable=False)
    new_price = Column(Float, nullable=False)

    goods = relationship('Good', lazy="immediate", primaryjoin='DiscountGood.goods_id == Good.goods_id', backref='discount_goods')


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'

    id = Column(Integer, primary_key=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DateTime, nullable=False)


class Doctor(Base):
    __tablename__ = 'doctors'

    d_id = Column(Integer, primary_key=True, unique=True)
    room_id = Column(ForeignKey('room.room_id'), nullable=False, index=True)
    d_name = Column(String(20), nullable=False)
    d_relname = Column(String(20), nullable=False)
    d_skill = Column(String(1000), nullable=False)
    d_head = Column(String(200), nullable=False)
    d_idcard = Column(String(20))
    d_cer = Column(String(256))
    is_order = Column(Integer, nullable=False, server_default=FetchedValue())

    room = relationship('Room', primaryjoin='Doctor.room_id == Room.room_id', backref='doctors')


class FollowDoc(Base):
    __tablename__ = 'follow_doc'

    fd_id = Column(Integer, primary_key=True, unique=True)
    u_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    d_id = Column(ForeignKey('doctors.d_id'), nullable=False, index=True)

    d = relationship('Doctor', lazy="immediate", primaryjoin='FollowDoc.d_id == Doctor.d_id', backref='follow_docs')
    u = relationship('User', primaryjoin='FollowDoc.u_id == User.id', backref='follow_docs')


class FollowGood(Base):
    __tablename__ = 'follow_good'

    fd_id = Column(Integer, primary_key=True, unique=True)
    u_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    goods_id = Column(ForeignKey('goods.goods_id'), nullable=False, index=True)

    goods = relationship('Good', lazy="immediate", primaryjoin='FollowGood.goods_id == Good.goods_id', backref='follow_goods')
    u = relationship('User', primaryjoin='FollowGood.u_id == User.id', backref='follow_goods')


class Forum(Base):
    __tablename__ = 'forum'

    f_id = Column(Integer, primary_key=True, unique=True)
    u_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    f_title = Column(String(100), nullable=False)
    f_content = Column(String(1000), nullable=False)

    u = relationship('User', lazy="immediate", primaryjoin='Forum.u_id == User.id', backref='forums')


class Good(Base):
    __tablename__ = 'goods'

    goods_id = Column(Integer, primary_key=True, unique=True)
    goods_name = Column(String(50), nullable=False)
    url = Column(String(256), nullable=False)
    price = Column(Float, nullable=False)
    medtype = Column(Integer, nullable=False)
    standards = Column(String(30), nullable=False)
    detail = Column(String(256), nullable=False)
    product_num = Column(String(20), nullable=False)
    product_name = Column(String(20), nullable=False)
    normal_name = Column(String(50), nullable=False)
    allow_num = Column(String(20), nullable=False)
    imgs = Column(String(512), nullable=False)
    introduce_img = Column(String(100), nullable=False)


class Hospital(Base):
    __tablename__ = 'hospitals'

    h_id = Column(Integer, primary_key=True, unique=True)
    cityid = Column(ForeignKey('city.cityid'), nullable=False, index=True)
    hname = Column(String(50), nullable=False)
    haddress = Column(String(100), nullable=False)
    hgrade = Column(String(20), nullable=False)
    htext = Column(String(200), nullable=False)

    city = relationship('City', primaryjoin='Hospital.cityid == City.cityid', backref='hospitals')


class Infomation(Base):
    __tablename__ = 'infomation'

    i_id = Column(Integer, primary_key=True, unique=True)
    titile = Column(String(50), nullable=False)
    content = Column(String(10000), nullable=False)


class Medtype(Base):
    __tablename__ = 'medtypes'

    m_id = Column(Integer, primary_key=True, unique=True)
    typenum = Column(Integer, nullable=False)
    medname = Column(String(50), nullable=False)


class Notice(Base):
    __tablename__ = 'notice'

    n_id = Column(Integer, primary_key=True, unique=True)
    s_id = Column(ForeignKey('sys_user.id'), nullable=False, index=True)
    n_text = Column(String(100), nullable=False)
    is_use = Column(Integer, nullable=False, server_default=FetchedValue())

    s = relationship('SysUser', primaryjoin='Notice.s_id == SysUser.id', backref='notices')


class Orderdetail(Base):
    __tablename__ = 'orderdetail'

    o_detail_id = Column(Integer, primary_key=True, unique=True)
    o_id = Column(ForeignKey('orderlist.o_id'), nullable=False, index=True)
    goods_id = Column(ForeignKey('goods.goods_id'), nullable=False, index=True)
    goods_num = Column(Integer, nullable=False)

    goods = relationship('Good', primaryjoin='Orderdetail.goods_id == Good.goods_id', backref='orderdetails')
    o = relationship('Orderlist', primaryjoin='Orderdetail.o_id == Orderlist.o_id', backref='orderdetails')


class Orderlist(Base):
    __tablename__ = 'orderlist'

    o_id = Column(Integer, primary_key=True, unique=True)
    o_identifier = Column(String(100), nullable=False, unique=True)
    u_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    o_price = Column(Float, nullable=False)
    o_time = Column(DateTime, nullable=False)
    o_nums = Column(Integer, nullable=False)
    a_id = Column(ForeignKey('user_address.a_id'), nullable=False, index=True)
    o_state = Column(Integer, nullable=False)

    a = relationship('UserAddres', primaryjoin='Orderlist.a_id == UserAddres.a_id', backref='orderlists')
    u = relationship('User', primaryjoin='Orderlist.u_id == User.id', backref='orderlists')


class Province(Base):
    __tablename__ = 'province'

    provinceid = Column(Integer, primary_key=True, unique=True)
    provincename = Column(String(20), nullable=False)


class Room(Base):
    __tablename__ = 'room'

    room_id = Column(Integer, primary_key=True, unique=True)
    h_id = Column(ForeignKey('hospitals.h_id'), nullable=False, index=True)
    roomname = Column(String(45), nullable=False)

    h = relationship('Hospital', primaryjoin='Room.h_id == Hospital.h_id', backref='rooms')


class RotationSelect(Base):
    __tablename__ = 'rotation_select'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    is_select = Column(Integer)


class Rotatiton(Base):
    __tablename__ = 'rotatitons'

    ro_id = Column(Integer, primary_key=True, unique=True)
    url = Column(String(256), nullable=False)


class SysRole(Base):
    __tablename__ = 'sys_role'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    code = Column(String(20), nullable=False, unique=True)


class SysUser(Base):
    __tablename__ = 'sys_user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    auth_string = Column(String(100), nullable=False)
    email = Column(String(50))
    phone = Column(String(50))


class SysUserRole(Base):
    __tablename__ = 'sys_user_role'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    role_id = Column(Integer)


class Translate(Base):
    __tablename__ = 'translate'

    id = Column(Integer, primary_key=True)
    english = Column(String(20), nullable=False)
    chinese = Column(String(20), nullable=False)


class UserAddres(Base):
    __tablename__ = 'user_address'

    a_id = Column(Integer, primary_key=True, unique=True)
    id = Column(ForeignKey('users.id'), nullable=False, index=True)
    provinceid = Column(ForeignKey('province.provinceid'), nullable=False, index=True)
    cityid = Column(ForeignKey('city.cityid'), nullable=False, index=True)
    user_name = Column(String(20), nullable=False)
    user_tel = Column(String(11), nullable=False)
    detail_address = Column(String(200), nullable=False)
    is_default = Column(Integer, nullable=False)

    city = relationship('City', primaryjoin='UserAddres.cityid == City.cityid', backref='user_address')
    user = relationship('User', primaryjoin='UserAddres.id == User.id', backref='user_address')
    province = relationship('Province', primaryjoin='UserAddres.provinceid == Province.provinceid', backref='user_address')


class UserInfo(Base):
    __tablename__ = 'user_info'

    ui_id = Column(Integer, primary_key=True, unique=True)
    u_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    u_height = Column(Float, nullable=False)
    u_weight = Column(Float, nullable=False)
    u_sex = Column(Integer, nullable=False)
    u_relname = Column(String(50))

    u = relationship('User', primaryjoin='UserInfo.u_id == User.id', backref='user_infos')


class UserNotice(Base):
    __tablename__ = 'user_notice'

    un_id = Column(Integer, primary_key=True, unique=True)
    u_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    un_titile = Column(String(50), nullable=False)
    un_text = Column(String(100), nullable=False)
    un_time = Column(String(10), nullable=False)

    u = relationship('User', lazy="immediate", primaryjoin='UserNotice.u_id == User.id', backref='user_notices')


class UserPaypal(Base):
    __tablename__ = 'user_paypal'

    up_id = Column(Integer, primary_key=True, unique=True)
    u_id = Column(ForeignKey('users.id'), nullable=False, unique=True)
    up_balance = Column(Float, nullable=False, server_default=FetchedValue())

    u = relationship('User', primaryjoin='UserPaypal.u_id == User.id', backref='user_paypals')


class Userauth(Base):
    __tablename__ = 'userauth'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    auth = Column(Integer)
    name = Column(String(20))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True)
    u_name = Column(String(20))
    u_password = Column(String(50), nullable=False)
    u_tel = Column(String(11), nullable=False, unique=True)
    u_image = Column(String(256))
