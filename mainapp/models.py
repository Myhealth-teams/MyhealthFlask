# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'

    id = Column(Integer, primary_key=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DateTime, nullable=False)


class Rotation(Base):
    __tablename__ = 'rotations'

    id = Column(Integer, primary_key=True)
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
    role_id = Column(Integer)
    sy_id = Column(Integer)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    u_name = Column(String(20))
    u_password = Column(String(50), nullable=False)
    u_tel = Column(String(11), nullable=False, unique=True)
    u_image = Column(String(256))
