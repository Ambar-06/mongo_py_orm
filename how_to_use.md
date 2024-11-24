# How to Use the MongoDB ORM Package with Django

This guide explains how to set up and use the MongoDB ORM package with a Django project. The package enables you to create MongoDB-based models in Django without relying on traditional relational databases. Follow the steps below to integrate and use the package in your Django project.

## 1. Configuration Setup

To configure your Django project for MongoDB:

1. **Update the `__init__.py` File**  
   In your Django project directory, locate the `__init__.py` file. Add the following snippet to configure your database:

   ```python
   from <project_name> import settings
   from mongo_client.client import MongoDBConfig

   DATABASE_NAME = settings.DATABASE_NAME
   DATABASE_USERNAME = settings.DATABASE_USERNAME
   CLUSTER_NAME = settings.CLUSTER_NAME
   DATABASE_PASSWORD = settings.DATABASE_PASSWORD

   config = MongoDBConfig()
   config.set_config(
       db_name=DATABASE_NAME, 
       username=DATABASE_USERNAME, 
       password=DATABASE_PASSWORD, 
       cluster_name=CLUSTER_NAME
   )

This snippet initializes the MongoDB configuration using the settings defined in your settings.py.

## 2. Comment Out the Relational Database Configuration
In the settings.py file of your Django project, comment out the default relational database configuration since it won't be used.
```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
```
## 3. Defining Models with the MongoDB ORM

Once your project is configured, you can start creating models using the package's custom fields. Here's an example of defining a model:

* Create a Model File
* In your Django app, create a new file, such as `models.py`.
* Import the Required Classes
* Import the field types and base model class from the `orm.mongo_orm` module:
```python
from orm.mongo_orm import CharField, FloatField, MongoModel, UUIDField
```

Here's an example of a model for User:
```python
class User(MongoModel):
    uuid = UUIDField(required=True, default=str(uuid.uuid4()))
    first_name = CharField(max_length=255, blank=True, default=None)
    last_name = CharField(max_length=255, blank=True, default=None)
    username = CharField(max_length=255, blank=True, default=None)
    email = CharField(max_length=255, blank=True, default=None) 
    phone_number = CharField(max_length=14, blank=True, default=None)
    country_code = CharField(max_length=5, blank=True, default=None)
    is_email_verified = BooleanField(default=False)
    password = CharField(max_length=255, blank=True, default=None)
    is_active = BooleanField(default=True)
    is_admin = BooleanField(default=False)
    is_staff = BooleanField(default=False)
    is_guest = BooleanField(default=False)
    last_login = DateTimeField(blank=True, default=None)
    is_deleted = BooleanField(default=False)
    created_at = DateTimeField(default=None)
    updated_at = DateTimeField(default=None)

    def __str__(self):
        return str(self._id)

    class Meta:
        collection_name = "users"
        indexes = [
            # Creating a unique compound index for country_code and phone_number
            {"keys": [("country_code", 1), ("phone_number", 1)], "unique": True}
        ]

# Initialize the manager
User._initialize_manager()
```
## 4. Using the MongoDB ORM Models

Once your model is set up, you can interact with the database using the MongoDB ORM's manager methods:

Create a Record:
```python
user = User(
    first_name="John",
    last_name="Doe",
    email="example@example.com",
    is_admin=True,
    last_login=datetime.utcnow().timestamp()
)
user.save()
```
Retrieve Records:
```python
users = User.objects.all()  # Fetch all records

specific_user = User.objects.get(_id=log_id)  # Fetch a record by ID
```
Update a Record:
```python
user.is_active = False
user.save()  # Updates the record in the database
```
Delete a Record:
```python
user.delete()  # Removes the record from the database
```
## Conclusion

This guide provides a simple setup to use MongoDB as the primary database in a Django project. By following these steps, you can define, manage, and manipulate MongoDB data seamlessly, leveraging the Django-like ORM provided by the package.

Feel free to extend your models by using other field types (IntegerField, BooleanField, etc.) available in the orm.mongo_orm package for more complex use cases.