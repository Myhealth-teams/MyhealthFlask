# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Cart(Base):
    __tablename__ = 'carts'

    c_id = Column(Integer, primary_key=True)
    u_id = Column(ForeignKey('users.id'), index=True)
    goods_id = Column(ForeignKey('goods.goods_id'), index=True)
    c_goods_num = Column(Integer, nullable=False)
    c_is_selected = Column(Integer, nullable=False)

    goods = relationship('Good', lazy="immediate", primaryjoin='Cart.goods_id == Good.goods_id', backref='carts')
    u = relationship('User', lazy="immediate", primaryjoin='Cart.u_id == User.id', backref='carts')


class City(Base):
    __tablename__ = 'city'

    cityid = Column(Integer, primary_key=True, unique=True)
    provinceid = Column(ForeignKey('province.provinceid'), index=True)
    cityname = Column(String(45))

    province = relationship('Province', lazy="immediate", primaryjoin='City.provinceid == Province.provinceid', backref='cities')


class DiscountGood(Base):
    __tablename__ = 'discount_goods'

    dg_id = Column(Integer, primary_key=True, unique=True)
    goods_id = Column(ForeignKey('goods.goods_id'), nullable=False, index=True)
    discount = Column(Float, nullable=False)
    new_price = Column(Float)

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
    room_id = Column(ForeignKey('room.room_id'), index=True)
    d_name = Column(String(20))
    d_relname = Column(String(20))
    d_skill = Column(String(1000))
    d_head = Column(String(200))
    d_idcard = Column(String(20))
    d_cer = Column(String(256))
    is_order = Column(Integer, nullable=False, server_default=FetchedValue())

    room = relationship('Room', lazy="immediate", primaryjoin='Doctor.room_id == Room.room_id', backref='doctors')


class FollowDoc(Base):
    __tablename__ = 'follow_doc'

    fd_id = Column(Integer, primary_key=True, unique=True)
    u_id = Column(ForeignKey('users.id'), index=True)
    d_id = Column(ForeignKey('doctors.d_id'), index=True)

    d = relationship('Doctor', lazy="immediate", primaryjoin='FollowDoc.d_id == Doctor.d_id', backref='follow_docs')
    u = relationship('User', lazy="immediate", primaryjoin='FollowDoc.u_id == User.id', backref='follow_docs')


class FollowGood(Base):
    __tablename__ = 'follow_good'

    fd_id = Column(Integer, primary_key=True, unique=True)
    u_id = Column(ForeignKey('users.id'), index=True)
    goods_id = Column(ForeignKey('goods.goods_id'), index=True)

    goods = relationship('Good', lazy="immediate", primaryjoin='FollowGood.goods_id == Good.goods_id', backref='follow_goods')
    u = relationship('User', lazy="immediate", primaryjoin='FollowGood.u_id == User.id', backref='follow_goods')


class Good(Base):
    __tablename__ = 'goods'

    goods_id = Column(Integer, primary_key=True)
    goods_name = Column(String(50))
    url = Column(String(256), nullable=False)
    price = Column(Float, nullable=False)
    medtype = Column(Integer, nullable=False)
    standards = Column(String(30), nullable=False)
    detial = Column(String(256))


class Hospital(Base):
    __tablename__ = 'hospitals'

    h_id = Column(Integer, primary_key=True, unique=True)
    cityid = Column(ForeignKey('city.cityid'), index=True)
    hname = Column(String(50))
    haddress = Column(String(100))
    hgrade = Column(String(20))
    htext = Column(String(200))

    city = relationship('City', lazy="immediate", primaryjoin='Hospital.cityid == City.cityid', backref='hospitals')


class Infomation(Base):
    __tablename__ = 'infomation'

    i_id = Column(Integer, primary_key=True, unique=True)
    titile = Column(String(50))
    content = Column(String(10000))


class Medtype(Base):
    __tablename__ = 'medtypes'

    m_id = Column(Integer, primary_key=True)
    typenum = Column(Integer, nullable=False)
    medname = Column(String(50), nullable=False)


class Province(Base):
    __tablename__ = 'province'

    provinceid = Column(Integer, primary_key=True, unique=True)
    provincename = Column(String(20))


class Room(Base):
    __tablename__ = 'room'

    room_id = Column(Integer, primary_key=True, unique=True)
    h_id = Column(ForeignKey('hospitals.h_id'), index=True)
    roomname = Column(String(45))

    h = relationship('Hospital', lazy="immediate", primaryjoin='Room.h_id == Hospital.h_id', backref='rooms')


class RotationSelect(Base):
    __tablename__ = 'rotation_select'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    is_select = Column(Integer)


class Rotatiton(Base):
    __tablename__ = 'rotatitons'

    ro_id = Column(Integer, primary_key=True)
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


class UserAddres(Base):
    __tablename__ = 'user_address'

    a_id = Column(Integer, primary_key=True, unique=True)
    id = Column(ForeignKey('users.id'), index=True)
    provinceid = Column(ForeignKey('province.provinceid'), index=True)
    cityid = Column(ForeignKey('city.cityid'), index=True)
    user_name = Column(String(20))
    user_tel = Column(String(11))
    detail_address = Column(String(200))
    is_default = Column(Integer)

    city = relationship('City', lazy="immediate", primaryjoin='UserAddres.cityid == City.cityid', backref='user_address')
    user = relationship('User', lazy="immediate", primaryjoin='UserAddres.id == User.id', backref='user_address')
    province = relationship('Province', lazy="immediate", primaryjoin='UserAddres.provinceid == Province.provinceid', backref='user_address')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    u_name = Column(String(20))
    u_password = Column(String(50), nullable=False)
    u_tel = Column(String(11), nullable=False, unique=True)
    u_image = Column(String(256))
