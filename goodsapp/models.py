# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, VARBINARY
from sqlalchemy.orm import relationship
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

    goods = relationship('Good', primaryjoin='Cart.goods_id == Good.goods_id', backref='carts')
    u = relationship('User', primaryjoin='Cart.u_id == User.id', backref='carts')


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'

    id = Column(Integer, primary_key=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DateTime, nullable=False)


class Good(Base):
    __tablename__ = 'goods'

    goods_id = Column(Integer, primary_key=True)
    goods_name = Column(VARBINARY(50), nullable=False)
    url = Column(String(256), nullable=False)
    price = Column(Float, nullable=False)
    medtype = Column(Integer, nullable=False)
    standards = Column(String(30), nullable=False)
    detial = Column(String(256))


class Medtype(Base):
    __tablename__ = 'medtypes'

    m_id = Column(Integer, primary_key=True)
    typenum = Column(Integer, nullable=False)
    medname = Column(String(50), nullable=False)


class RotationStatu(Base):
    __tablename__ = 'rotation_status'

    rs_id = Column(Integer, primary_key=True)
    ro_id = Column(ForeignKey('rotatitons.ro_id'), index=True)
    rs_name = Column(String(10), nullable=False)

    ro = relationship('Rotatiton', primaryjoin='RotationStatu.ro_id == Rotatiton.ro_id', backref='rotation_status')


class Rotatiton(Base):
    __tablename__ = 'rotatitons'

    ro_id = Column(Integer, primary_key=True)
    url = Column(String(256), nullable=False)


class SysRole(Base):
    __tablename__ = 'sys_role'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(50), nullable=False)
    role_code = Column(String(20), nullable=False)


class SysUser(Base):
    __tablename__ = 'sys_user'

    sy_id = Column(Integer, primary_key=True)
    sy_name = Column(String(50))
    auth_string = Column(String(100))
    email = Column(String(50))


class SysUserRole(Base):
    __tablename__ = 'sys_user_role'

    sr_id = Column(Integer, primary_key=True)
    role_id = Column(ForeignKey('sys_role.role_id'), index=True)
    sy_id = Column(ForeignKey('sys_user.sy_id'), index=True)

    role = relationship('SysRole', primaryjoin='SysUserRole.role_id == SysRole.role_id', backref='sys_user_roles')
    sy = relationship('SysUser', primaryjoin='SysUserRole.sy_id == SysUser.sy_id', backref='sys_user_roles')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    u_name = Column(String(20))
    u_password = Column(String(50), nullable=False)
    u_tel = Column(String(11), nullable=False, unique=True)
    u_image = Column(String(256))
