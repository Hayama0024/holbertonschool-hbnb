from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.amenity_repository import AmenityRepository
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repository = UserRepository()
        self.place_repository = PlaceRepository()
        self.review_repository = ReviewRepository()
        self.amenity_repository = AmenityRepository()

    def create_user(self, user_data):
        return self.user_repository.create(user_data)

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repository.get_user_by_email(email)

    def update_user(self, user_id, update_data):
        user = self.user_repository.get(user_id)
        if not user:
            return None
        return self.user_repository.update(user, **update_data)

    def get_all_users(self):
        return self.user_repository.get_all()

    def delete_user(self, user_id):
        return self.user_repository.delete(user_id)

    def create_amenity(self, data):
        amenity = Amenity(name=data['name'])
        self.amenity_repository.add(amenity)
        return amenity

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def update_amenity(self, amenity_id, data):
        return self.amenity_repository.update(amenity_id, data)

    def delete_amenity(self, amenity_id):
        return self.amenity_repository.delete(amenity_id)

    def create_place(self, place_data):
        price = place_data.get('price')
        latitude = place_data.get('latitude')
        longitude = place_data.get('longitude')

        if price is None or price < 0:
            raise ValueError("Price must be a non-negative float.")
        if latitude is None or not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if longitude is None or not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        owner_id = place_data.get('owner_id')
        owner = self.user_repository.get(owner_id)
        if not owner:
            raise ValueError("The specified owner does not exist.")

        amenities_names = place_data.get('amenities', [])
        amenities = []
        for name in amenities_names:
            amenity = next(
                (a for a in self.amenity_repository.get_all() if a.name == name),
                None
            )
            if not amenity:
                raise ValueError(f"Amenity not found: {name}")
            amenities.append(amenity)

        place = Place(
            title=place_data['title'],
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner_id=owner.id,
            description=place_data.get('description', "")
        )

        place.amenities = amenities
        self.place_repository.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repository.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        return place

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, place_data):
        if 'price' in place_data and place_data['price'] < 0:
            raise ValueError("Price must be a non-negative float.")
        if 'latitude' in place_data and not (-90 <= place_data['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if 'longitude' in place_data and not (-180 <= place_data['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        if 'owner_id' in place_data:
            owner = self.user_repository.get(place_data['owner_id'])
            if not owner:
                raise ValueError("The specified owner does not exist.")
            place_data['owner'] = owner
            del place_data['owner_id']

        if 'amenities' in place_data:
            amenity_names = place_data['amenities']
            amenities = []
            for name in amenity_names:
                amenity = next(
                    (a for a in self.amenity_repository.get_all() if a.name == name),
                    None
                )
                if not amenity:
                    raise ValueError(f"Amenity not found: {name}")
                amenities.append(amenity)
            place_data['amenities'] = amenities

        return self.place_repository.update(place_id, place_data)

    def create_review(self, review_data):
        user_identifier = review_data.get('user_id')
        place_identifier = review_data.get('place_id')

        user = self.user_repository.get_by_attribute("email", user_identifier)
        if not user:
            user = self.user_repository.get_by_attribute("first_name", user_identifier)
        if not user:
            raise ValueError("The specified user does not exist.")

        place = self.place_repository.get(place_identifier)
        if not place:
            place = self.place_repository.get_by_attribute("title", place_identifier)
        if not place:
            raise ValueError("The specified place does not exist.")

        rating = review_data.get('rating')
        text = review_data.get('text')

        if rating is None or not (0 <= rating <= 5):
            raise ValueError("Rating must be between 0 and 5.")

        review = Review(text=text, rating=rating, user=user, place=place)
        self.review_repository.add(review)
        return review

    def get_review(self, review_id):
        review = self.review_repository.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        return review

    def get_all_reviews(self):
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repository.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        return place.reviews

    def update_review(self, review_id, data):
        if 'rating' in data and not (0 <= data['rating'] <= 5):
            raise ValueError("Rating must be between 0 and 5.")
        return self.review_repository.update(review_id, data)

    def delete_review(self, review_id):
        return self.review_repository.delete(review_id)
