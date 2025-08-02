from app.models import BaseModel
from app import db
from sqlalchemy.orm import relationship

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    # ここは既存のスキーマに合わせています（String(36)）
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # ユーザー側の backref はそのままでもOK
    user = relationship('User', backref='reviews')

    # ★ 衝突回避：backref → back_populates に変更（Place 側と対）
    place = relationship('Place', back_populates='reviews')

    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("Review text is required")
        # API側(モデル/エンドポイント)で 0..5 にしているので統一
        if not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5")
        if not place or not hasattr(place, 'id'):
            raise ValueError("Invalid place")
        if not user or not hasattr(user, 'id'):
            raise ValueError("Invalid user")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id if self.user else None,
            'place_id': self.place.id if self.place else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_dict_get(self):
        # フロントの表示に使う軽量版。必要なら user の名前も付与
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user': {
                'id': self.user.id,
                'first_name': getattr(self.user, 'first_name', None)
            } if self.user else None
        }
