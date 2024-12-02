import uuid

from bson.objectid import ObjectId
import datetime
from mongo_client.client import Client

db = Client().connect()

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
        if self.required and value is None:
            raise ValueError("This field is required")
        if value is None:
            return None
        if not isinstance(value, float):
            raise ValueError("Expected an float")
        return value


class BooleanField(Field):
    def __init__(self, default=None, required=False):
        super().__init__(required, default)

    def to_python(self, value):
        if self.required and value is None:
            raise ValueError("This field is required")
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
        if self.required and value is None:
            raise ValueError("This field is required")
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
    def __init__(self, auto_now=False, auto_now_add=False, **kwargs):
        super().__init__(**kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
        
    def to_python(self, value):
        if self.auto_now:
            return datetime.now()
        if self.auto_now_add and value is None:
            return datetime.now() 
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

class QuerySet:
    """A wrapper for query results, allowing for further operations like `.first()`."""

    def __init__(self, model_class, documents_cursor, filter_criteria=None):
        self.model_class = model_class
        self.documents_cursor = documents_cursor    # Cursor from the MongoDB query
        self.filter_criteria = filter_criteria or {} 

    def __iter__(self):
        """Allow the QuerySet to be iterable."""
        """Make the QuerySet iterable."""
        try:
            docs = [self.model_class(**doc) for doc in self.documents_cursor]
            return iter(docs)
        except Exception as e:
            return iter([])

    def first(self):
        """Return the first document if available."""
        first_document = next(self.documents_cursor, None)
        if first_document:
            return self.model_class(**first_document)
        return None
    
    def exclude(self, **kwargs):
        """Exclude documents matching the given kwargs."""
        excluded_docs = [
            doc for doc in self.documents_cursor
            if not all(item in doc.items() for item in kwargs.items())
        ]
        return [self.model_class(**doc) for doc in excluded_docs]

    def count(self):
        """Count the number of documents in the QuerySet."""
        # Use count_documents with the filter criteria if available
        if self.filter_criteria:
            return self.documents_cursor.collection.count_documents(self.filter_criteria)
        # Fallback to counting the cursor length if filter criteria are not stored
        return len(list(self.documents_cursor))
    
    def delete(self):
        """Delete all documents in the QuerySet."""
        for doc in self.documents_cursor:
            self.model_class(**doc).delete()



class MongoManager:
    def __init__(self, model_class):
        self.model_class = model_class
        self.collection = db[model_class.Meta.collection_name]

    def all(self):
        """Fetch all documents from the collection."""
        documents_cursor = self.collection.find()
        return QuerySet(self.model_class, documents_cursor)

    def filter(self, **kwargs):
        """
        Filter documents by the given kwargs, supporting `__in` for fields.
        """
        mongo_query = {}
        
        for key, value in kwargs.items():
            if "__" in key:
                field_name, lookup = key.split("__", 1)

                if lookup == "in":
                    if field_name == "_id":
                        value = [ObjectId(v) for v in value]
                    mongo_query[field_name] = {"$in": value}

                elif lookup == "contains":
                    if not isinstance(value, str):
                        raise ValueError("The `contains` filter expects a string value.")
                    mongo_query[field_name] = {"$regex": f"{value}"}

                elif lookup == "icontains":
                    if not isinstance(value, str):
                        raise ValueError("The `icontains` filter expects a string value.")
                    # Case-insensitive matching using $regex and $options: "i"
                    mongo_query[field_name] = {"$regex": f"{value}", "$options": "i"}

                else:
                    raise ValueError(f"Unsupported lookup: {lookup}")
            else:
                if key == "_id":
                    value = ObjectId(value)
                mongo_query[key] = value
        
        # Query MongoDB with the converted query
        try:
            documents_cursor = self.collection.find(mongo_query)
            return QuerySet(self.model_class, self.collection.find(mongo_query), filter_criteria=kwargs)
        except Exception as e:
            print("Error Executing Query:", str(e))
            return QuerySet(self.model_class, [], filter_criteria=kwargs)

    def exclude(self, **kwargs):
        """Exclude documents by the given kwargs."""
        documents_cursor = self.collection.find()
        return QuerySet(
            self.model_class,
            [
                doc for doc in documents_cursor
                if not all(item in doc.items() for item in kwargs.items())
            ]
        )

    def get(self, **kwargs):
        """Get a single document matching the kwargs."""
        document = self.collection.find_one(kwargs)
        if document:
            return self.model_class(**document)
        raise ValueError(f"No document found matching: {kwargs}")

    def create(self, **kwargs):
        """Create a new document in the collection."""
        current_time = datetime.datetime.now()
        document = {}
        fields = self.model_class._get_fields()
        for key, field in fields.items():
            value = kwargs.get(key, field.default)

            # Handle auto_now_add fields
            if isinstance(field, DateTimeField):
                if field.auto_now_add:
                    value = current_time
                if field.auto_now:
                    value = current_time

            # Handle required fields
            if value is None and field.required:
                raise ValueError(f"Field '{key}' is required.")

            document[key] = value
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
        current_time = datetime.datetime.now()
        data = {}
        for key, field in self._get_fields().items():
            value = getattr(self, key)

            if isinstance(field, DateTimeField):
                # Handle auto_now
                if field.auto_now:
                    value = current_time
                    setattr(self, key, value)
            if isinstance(field, DateTimeField):
                if field.auto_now_add and self._id is None:
                    value = current_time
                    setattr(self, key, value)

            # Prepare data for saving
            data[key] = value

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
