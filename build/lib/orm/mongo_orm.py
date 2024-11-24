import uuid

from bson.objectid import ObjectId
import datetime
from mongo_client.client import db

class Field:
    def __init__(self, required=False, default=None, blank=False):
        self.required = required
        self.default = default
        self.blank = blank

    def to_python(self, value):
        return value


class CharField(Field):
    def __init__(self, max_length=None, blank=False, **kwargs):
        super().__init__(**kwargs)  # Pass only the valid kwargs to Field
        self.max_length = max_length
        self.blank = blank  # Store blank information if necessary

    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("Expected a string")
        if self.max_length and len(value) > self.max_length:
            raise ValueError(f"Value exceeds max length of {self.max_length}")
        return value


class IntegerField(Field):
    def __init__(self, default=None):
        super().__init__(default=default)

    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, int):
            raise ValueError("Expected an integer")
        return value


class FloatField(Field):
    def __init__(self, default=None, required=False):
        super().__init__(required, default)

    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, float):
            raise ValueError("Expected an float")
        return value


class BooleanField(Field):
    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, bool):
            raise ValueError("Expected an boolean")
        return value


class ListField(Field):
    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, list):
            raise ValueError("Expected an list")
        return value


class JSONField(Field):
    def to_python(self, value):
        if value is None:
            return None
        if type(value) not in [list, dict]:
            raise ValueError("Expected an list or dict")
        return value


class UUIDField(Field):
    def __init__(self, default=None, required=False):
        super().__init__(required, default)

    def to_python(self, value):
        if value is None:
            return None
        if not isinstance(value, uuid.UUID):
            raise ValueError("Expected an UUID")
        return value
    
class DateField(Field):
    def __init__(self, default=None, required=False):
        super().__init__(required, default)

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                # Try to parse a date string into a date object
                value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Expected a valid date string in 'YYYY-MM-DD' format")
        if not isinstance(value, datetime.date):
            raise ValueError("Expected a date object or a valid date string")
        return value


class DateTimeField(Field):
    def __init__(self, default=None, required=False, blank=True):
        super().__init__(required, default, blank)
        
    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, str):
            try:
                # Try to parse a datetime string into a datetime object
                value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError("Expected a valid datetime string in 'YYYY-MM-DD HH:MM:SS' format")
        if not isinstance(value, datetime.datetime):
            raise ValueError("Expected a datetime object or a valid datetime string")
        return value


class MongoManager:
    def __init__(self, model_class):
        self.model_class = model_class
        self.collection = db[model_class.Meta.collection_name]

    def all(self):
        """Fetch all documents from the collection."""
        documents = self.collection.find()
        return [self.model_class(**doc) for doc in documents]

    def filter(self, **kwargs):
        """Filter documents by the given kwargs."""
        documents = self.collection.find(kwargs)
        return [self.model_class(**doc) for doc in documents]

    def get(self, **kwargs):
        """Get a single document matching the kwargs."""
        document = self.collection.find_one(kwargs)
        if document:
            return self.model_class(**document)
        raise ValueError(f"No document found matching: {kwargs}")

    def create(self, **kwargs):
        """Create a new document in the collection."""
        document = kwargs
        result = self.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return self.model_class(**document)


class MongoModel:
    objects = None

    def __init__(self, **kwargs):
        self._id = kwargs.get("_id")
        for key, value in self._get_fields().items():
            field_value = kwargs.get(key, value.default)
            setattr(self, key, field_value)

    def save(self):
        data = {key: getattr(self, key) for key in self._get_fields()}
        if self._id:
            self.objects.collection.update_one(
                {"_id": ObjectId(self._id)}, {"$set": data}
            )
        else:
            result = self.objects.collection.insert_one(data)
            self._id = result.inserted_id

    def delete(self):
        if self._id:
            self.objects.collection.delete_one({"_id": ObjectId(self._id)})
        else:
            raise ValueError("Cannot delete an unsaved object.")

    @classmethod
    def _initialize_manager(cls):
        """Initialize the `objects` attribute with a MongoManager."""
        cls.objects = MongoManager(cls)

    @classmethod
    def _get_fields(cls):
        """Get all fields defined in the class."""
        return {
            key: value
            for key, value in cls.__dict__.items()
            if isinstance(value, Field)
        }
