# app/models/place.py
from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import String, Float, Text
from app.models.amenity import Amenity, place_amenities  # place_amenities を変数参照
import uuid  # ★ 追加：Python側でUUID採番

class Place(db.Model):
    __tablename__ = 'places'

    # ★ 変更点：default で UUID を自動採番（新規 INSERT 時に自動で入る）
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    title = db.Column(String(255), nullable=False)
    description = db.Column(Text, nullable=True)

    latitude = db.Column(Float, nullable=False)
    longitude = db.Column(Float, nullable=False)

    # プロジェクト方針: price を採用（フロント互換用に price_by_night も返す）
    price = db.Column(Float, nullable=False)

    owner_id = db.Column(String(36), db.ForeignKey('users.id'), nullable=False)
    owner = relationship('User', backref=db.backref('places', lazy=True))

    amenities = relationship(
        'Amenity',
        secondary=place_amenities,
        lazy='joined',  # 一覧で使うなら eager のままでOK
        backref=db.backref('places', lazy='dynamic')
    )

    reviews = relationship(
        'Review',
        back_populates='place',
        lazy=True,
        cascade="all, delete-orphan"
    )

    # ---- シリアライズ ----
    def _owner_dict(self):
        """フロントで使いやすい owner 表現"""
        o = self.owner
        if not o:
            return None
        full_name = f"{(o.first_name or '').strip()} {(o.last_name or '').strip()}".strip()
        return {
            "id": o.id,
            "name": full_name or (getattr(o, "email", None) or "Unknown")
        }

    def _amenities_list(self):
        """[{id, name}] の配列で返す（フロントがそのまま表示可能）"""
        return [{"id": a.id, "name": a.name} for a in (self.amenities or [])]

    def to_dict(self):
        """一覧/API用の基本形。price のキー揺れに対応。"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "price": self.price,
            "price_by_night": self.price,  # フロント互換
            "owner_id": self.owner_id,
        }

    def to_dict_detail(self):
        """詳細表示用。owner / amenities / reviews_count を含める"""
        base = self.to_dict()
        base.update({
            "owner": self._owner_dict(),
            "amenities": self._amenities_list(),
            "reviews_count": len(self.reviews or []),
        })
        return base

    def to_dict_get(self):
        # 既存の設計を踏襲：GET の詳細は detail を返す
        return self.to_dict_detail()
