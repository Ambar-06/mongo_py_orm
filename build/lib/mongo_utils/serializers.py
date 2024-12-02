from .mongo_orm import BooleanField, DateField, DateTimeField, UUIDField, QuerySet
import uuid
import datetime
from bson import ObjectId

class MongoSerializer:
    def __init__(self, instance=None, data=None, partial=False, many=False, context=None):
        """
        Initialize the serializer with an instance or data for validation.
        
        Args:
            instance (MongoModel or list): A single model instance or a list of instances.
            data (dict or list): Data to validate and deserialize (can be a list of dictionaries if `many=True`).
            partial (bool): If True, allows partial updates (some fields can be missing).
            many (bool): If True, serializes multiple instances (can be a list of objects).
        """
        self.instance = instance
        self.initial_data = data
        self.partial = partial
        self.many = many
        self.errors = {}
        self.validated_data = {}
        self.context = context

    def _get_fields(self):
        """Retrieve the fields from the associated model class."""
        if self.instance:
            return self.instance._get_fields()
        raise ValueError("No instance provided for determining fields.")

    def is_valid(self):
        """Validate the initial data against the model's fields."""
        if self.many:
            return all(self._validate_instance(item) for item in self.initial_data)
        else:
            return self._validate_instance(self.initial_data)

    def _validate_instance(self, data):
        """Validate a single instance's data."""
        fields = self._get_fields()
        for field_name, field_obj in fields.items():
            value = data.get(field_name, field_obj.default)

            # If the field is required and value is missing, add an error.
            if field_obj.required and value is None and not self.partial:
                self.errors[field_name] = "This field is required."
            else:
                # Try to convert the value to the correct type.
                try:
                    self.validated_data[field_name] = field_obj.to_python(value)
                except ValueError as e:
                    self.errors[field_name] = str(e)

        # Return True if no errors are found.
        return len(self.errors) == 0

    def save(self):
        """Save the validated data to the database, either updating or creating."""
        if not self.is_valid():
            raise ValueError(f"Invalid data: {self.errors}")

        if self.many:
            # Handle saving multiple instances
            instances = []
            for data in self.initial_data:
                instance = self._save_instance(data)
                instances.append(instance)
            return instances
        else:
            # Save a single instance
            return self._save_instance(self.validated_data)

    def _save_instance(self, data):
        """Helper method to save a single instance."""
        model_class = self._get_model_class()
        instance = model_class(**data)
        instance.save()
        return instance

    def to_representation(self, instance=None):
        """
        Convert the instance or list of instances to a dictionary representation.
        Handles both individual instances and lists/QuerySets of instances.

        Args:
            instance: A single instance or a list/QuerySet of instances to be serialized.

        Returns:
            dict or list: Serialized representation of the instance(s).
        """
        fields = self._get_fields()
        data = {}
        instance = instance or self.instance

        # Handle individual instance serialization
        if isinstance(instance, self._get_model_class()):
            # Serialize fields for the instance
            for field_name, field_serializer in fields.items():
                value = getattr(instance, field_name, None)
                if callable(field_serializer):
                    # Handle SerializerMethodField-like fields
                    data[field_name] = field_serializer(instance)
                else:
                    data[field_name] = field_serializer.to_representation(value)

            # Add MongoDB `_id` field as string if it exists
            if hasattr(instance, "_id") and isinstance(instance._id, ObjectId):
                data["_id"] = str(instance._id)

            return data

        # Handle list/QuerySet serialization
        if isinstance(instance, (list, QuerySet)):
            return [self.to_representation(obj) for obj in instance]

        raise ValueError(
            f"Unsupported type for serialization: {type(instance)}. Expected model instance, list, or QuerySet."
        )

    def _instance_to_dict(self, instance):
        """Convert a single instance to a dictionary."""
        data = {}
        for field_name, field_obj in self._get_fields().items():
            value = getattr(instance, field_name)
            data[field_name] = self._field_to_representation(field_obj, value)
        return data

    def _field_to_representation(self, field_obj, value):
        """Convert a field's value to a representation suitable for JSON."""
        if isinstance(field_obj, UUIDField) and isinstance(value, uuid.UUID):
            return str(value)
        if isinstance(field_obj, DateTimeField) and isinstance(value, datetime.datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(field_obj, DateField) and isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        if isinstance(field_obj, BooleanField):
            return bool(value)
        return value

    def _get_model_class(self):
        """Retrieve the associated model class (only relevant if creating)."""
        if self.instance:
            return self.instance.__class__
        raise ValueError("No instance provided to determine model class.")

    @property
    def data(self):
        """Property to get the serialized data."""
        return self.to_representation()
