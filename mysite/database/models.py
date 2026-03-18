from .db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date, DateTime, Enum, ForeignKey, Text, Boolean
from enum import Enum as PyEnum
from typing import List, Optional
from datetime import date, datetime


class RoleChoices(str, PyEnum):
    seller = 'seller'
    buyer = 'buyer'

class PropertyType(str, PyEnum):
    apartment = 'apartment'
    house = 'house'
    room = 'room'
    plot = 'plot'
    dacha = 'dacha'
    parking = 'parking'

class ConditionType(str, PyEnum):
    self_finishing = 'self_finishing'
    euro_renovation = 'euro_renovation'
    good = 'good'
    average = 'average'
    not_completed = 'not_completed'


class UserProfile(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[Optional[RoleChoices]] = mapped_column(Enum(RoleChoices), default=RoleChoices.buyer, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    avatar: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_date: Mapped[Date] = mapped_column(Date, default=date.today)

    pro_seller: Mapped[List['Property']] = relationship(back_populates='seller_pro', cascade='all, delete-orphan')
    review_author: Mapped[List['Review']] = relationship(back_populates='author_review', foreign_keys='Review.author_id', cascade='all, delete-orphan')
    review_seller: Mapped[List['Review']] = relationship(back_populates='seller_review', foreign_keys='Review.seller_id', cascade='all, delete-orphan')
    token_user: Mapped[List['RefreshToken']] = relationship(back_populates='user_token', cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'


class RefreshToken(Base):
    __tablename__ = 'refresh_token'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    token: Mapped[str] = mapped_column(String)
    created_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user_token: Mapped[UserProfile] = relationship(back_populates='token_user')


class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_name: Mapped[str] = mapped_column(String(64))

    reg_country: Mapped[List['Region']] = relationship(back_populates='country', cascade='all, delete-orphan')

    def __repr__(self):
        return self.country_name

class Region(Base):
    __tablename__ = 'region'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_id: Mapped[int] = mapped_column(ForeignKey('country.id'))
    region_name: Mapped[str] = mapped_column(String(64))

    country: Mapped[Country] = relationship(back_populates='reg_country')
    reg_city: Mapped[List['City']] = relationship(back_populates='region', cascade='all, delete-orphan')
    pro_region: Mapped[List['Property']] = relationship(back_populates='region_pro', cascade='all, delete-orphan')

    def __repr__(self):
        return self.region_name

class City(Base):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    region_id: Mapped[int] = mapped_column(ForeignKey('region.id'))
    city_name: Mapped[str] = mapped_column(String(64))
    city_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    region: Mapped[Region] = relationship(back_populates='reg_city')
    dis_city: Mapped[List['District']] = relationship(back_populates='city', cascade='all, delete-orphan')
    city_pro: Mapped[List['Property']] = relationship(back_populates='pro_city', cascade='all, delete-orphan')

    def __repr__(self):
        return self.city_name

class District(Base):
    __tablename__ = 'district'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    district_name: Mapped[str] = mapped_column(String(64), nullable=True)

    city: Mapped[City] = relationship(back_populates='dis_city')
    pro_district: Mapped[List['Property']] = relationship(back_populates='district_pro', cascade='all, delete-orphan')

    def __repr__(self):
        return self.district_name


class Property(Base):
    __tablename__ = 'property'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    property_type: Mapped[PropertyType] = mapped_column(Enum(PropertyType), default=PropertyType.room)
    seller_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    region_id: Mapped[int] = mapped_column(ForeignKey('region.id'))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    district_id: Mapped[int] = mapped_column(ForeignKey('district.id'))
    address: Mapped[str] = mapped_column(String(150))
    area: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    rooms: Mapped[int] = mapped_column(Integer)
    floor: Mapped[int] = mapped_column(Integer)
    total_floors: Mapped[int] = mapped_column(Integer)
    condition: Mapped[ConditionType] = mapped_column(Enum(ConditionType))
    documents: Mapped[bool] = mapped_column(Boolean)

    seller_pro: Mapped[UserProfile] = relationship(back_populates='pro_seller')
    region_pro: Mapped[Region] = relationship(back_populates='pro_region')
    pro_city: Mapped[City] = relationship(back_populates='city_pro')
    district_pro: Mapped[District] = relationship(back_populates='pro_district')
    property_img: Mapped[List['PropertyImages']] = relationship(back_populates='property', cascade='all, delete-orphan')

    def __repr__(self):
        return self.title


class PropertyImages(Base):
    __tablename__ = 'property_image'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    property_id: Mapped[int] = mapped_column(ForeignKey('property.id'))
    property_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    property: Mapped[Property] = relationship(back_populates='property_img')


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    rating: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    author_review: Mapped[UserProfile] = relationship(back_populates='review_author', foreign_keys=[author_id])
    seller_review: Mapped[UserProfile] = relationship(back_populates='review_seller', foreign_keys=[seller_id])
