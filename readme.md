# MongoPyORM

MongoPyORM is a lightweight Python Object-Relational Mapper (ORM)-like implementation for MongoDB. It provides a familiar and simple interface for defining and interacting with MongoDB documents using Python classes. This library is designed to help developers manage MongoDB data in an object-oriented way, similar to how traditional ORMs work with SQL databases.

## Features

- Define document models using Python classes.
- Built-in support for common field types such as:
  - `CharField`, `IntegerField`, `FloatField`, `BooleanField`, `ListField`, `JSONField`, `UUIDField`, `DateField`, `DateTimeField`.
- Simple CRUD operations with `MongoManager`.
- Field validation with custom data types.
- Supports relationships with embedded or referenced documents.

## Installation

To install MongoPyORM, use pip:

```bash
pip install MongoPyORM
```

## Quick Start

### 1. Configuration Setup

To configure your Django project for MongoDB:

1. **Update the `__init__.py` File**  
   In your Django project directory, locate the `__init__.py` file and add the following snippet to configure your database:

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
   ```

This snippet initializes the MongoDB configuration using the settings defined in your `settings.py`.

### 2. Comment Out the Relational Database Configuration

In the `settings.py` file of your Django project, comment out the default relational database configuration, as it won't be used with MongoDB:

```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
```

### 3. Defining Models with MongoPyORM

Once your project is configured, you can start creating models using the package's custom fields. Here's an example of defining a model:

- **Create a Model File**  
  In your Django app, create a new file, such as `models.py`.

- **Import the Required Classes**  
  Import the field types and base model class from the `orm.mongo_orm` module:

  ```python
  from mongo_utils.mongo_orm import CharField, FloatField, MongoModel, UUIDField
  ```

- **Define Your Model**  
  Create a Python class that inherits from `MongoModel` and define your fields:

  ```python
  from mongo_utils.mongo_orm import MongoModel, CharField, IntegerField, BooleanField

  class User(MongoModel):
      username = CharField(max_length=150, required=True)
      email = CharField(max_length=255)
      age = IntegerField(default=0)
      is_active = BooleanField(default=True)

      class Meta:
          collection_name = "users"
  ```

- **Initialize the Manager**  
  Call `_initialize_manager()` on the model to set up the manager for database operations:

  ```python
  User._initialize_manager()
  ```

### 4. Using the Model

- **Create a New User:**

  ```python
  user = User(username="john_doe", email="john@example.com", age=25)
  user.save()  # Save to the database
  ```

- **Query Users:**

  - **Get all users:**

    ```python
    users = User.objects.all()
    ```

  - **Filter users:**

    ```python
    active_users = User.objects.filter(is_active=True)
    ```

  - **Get a single user:**

    ```python
    john = User.objects.get(username="john_doe")
    ```

- **Update a User:**

  ```python
  john.age = 26
  john.save()  # Updates the existing document
  ```

- **Delete a User:**

  ```python
  john.delete()
  ```

## Field Types

The following field types are supported:

- `CharField`: For storing strings with optional `max_length`.
- `IntegerField`: For storing integers.
- `FloatField`: For storing floating-point numbers.
- `BooleanField`: For storing boolean values.
- `ListField`: For storing lists.
- `JSONField`: For storing JSON-compatible data (list or dict).
- `UUIDField`: For storing UUID values.
- `DateField`: For storing dates.
- `DateTimeField`: For storing datetime values.

### Customization

Each field has the following optional attributes:

- `required`: Whether the field is mandatory.
- `default`: A default value for the field if none is provided.
- `blank`: Whether the field can be left blank.

## Configuration

MongoPyORM uses MongoDB credentials (e.g., username, password, database name, and cluster name) for establishing the connection. You can configure your credentials by creating a `MongoDBConfig` class, as demonstrated below:

```python
from mongo_client.client import MongoDBConfig

# Set up MongoDB credentials globally
config = MongoDBConfig()
config.set_config(db_name="your_db", username="your_username", password="your_password", cluster_name="your_cluster")

# Now you can use MongoPyORM models with these credentials
```

Once credentials are configured, models will automatically use the provided settings for MongoDB interactions.

## Contributing

Contributions are welcome! Please follow the standard GitHub workflow (fork, feature branch, pull request workflow):

- Fork the repository.
- Create a feature branch (`git checkout -b feature/your-feature`).
- Commit your changes (`git commit -m 'Add your feature'`).
- Push to the branch (`git push origin feature/your-feature`).
- Open a pull request.

## License

This project is licensed under the MIT License.

## Future Enhancements

- Support for relationship fields (e.g., ForeignKey-like references).
- Query optimizations for large datasets.
- More advanced data validation.

## Issues

If you encounter any bugs or issues, feel free to open an issue on GitHub.

## Acknowledgments

This project was inspired by the simplicity of traditional ORMs and the power of MongoDB, aiming to bring them together seamlessly.

## Contact

For any inquiries or support, please contact [brannstrom9911@gmail.com].
