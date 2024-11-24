# MongoPyORM

MongoPyORM is a lightweight Python Object-Relational Mapper (ORM)-like implementation for MongoDB. It provides a familiar and simple interface for defining and interacting with MongoDB documents using Python classes. This library is designed to help developers manage MongoDB data in an object-oriented way, similar to how traditional ORMs work with SQL databases.

## Features

- Define document models using Python classes.
- Built-in support for common field types such as `CharField`, `IntegerField`, `FloatField`, `BooleanField`, `ListField`, `JSONField`, `UUIDField`, `DateField`, and `DateTimeField`.
- Simple CRUD operations with `MongoManager`.
- Field validation with custom data types.
- Supports relationships with embedded or referenced documents.

## Installation

To install MongoPyORM, use pip:
```bash
pip install mongopyorm
```
## Quick Start

1. Define Your Model
Create a Python class that inherits from MongoModel and define your fields:
```python
from mongopyorm import MongoModel, CharField, IntegerField, BooleanField

class User(MongoModel):
    username = CharField(max_length=150, required=True)
    email = CharField(max_length=255)
    age = IntegerField(default=0)
    is_active = BooleanField(default=True)

    class Meta:
        collection_name = "users"
```
2. Initialize the Manager
Call `_initialize_manager()` on the model to set up the manager for database operations:
```python
User._initialize_manager()
```
3. Using the Model
Create a new user
```python
user = User(username="john_doe", email="john@example.com", age=25)
user.save()  # Save to the database
```
### Query Users

4. Get all users
```python
users = User.objects.all()
```

5. Filter users
```python
active_users = User.objects.filter(is_active=True)
```

6. Get a single user
```python
john = User.objects.get(username="john_doe")
```
7. Update a User
```python
john.age = 26
john.save()  # Updates the existing document
```
8. Delete a User
```python
john.delete()
```
## Field Types

### The following field types are supported:

`CharField`: For storing strings with optional max_length.\
`IntegerField`: For storing integers.\
`FloatField`: For storing floating-point numbers.\
`BooleanField`: For storing boolean values.\
`ListField`: For storing lists.\
`JSONField`: For storing JSON-compatible data (list or dict).\
`UUIDField`: For storing UUID values.\
`DateField`: For storing dates.\
`DateTimeField`: For storing datetime values.\
Customization

### Each field has the following optional attributes:

`required`: Whether the field is mandatory.\
`default`: A default value for the field if none is provided.\
`blank`: Whether the field can be left blank.\

## Configuration

MongoPyORM uses MongoDB credentials (e.g., username, password, database name, and cluster name) for establishing the connection. You can configure your credentials by creating a `MongoDBConfig` class, as demonstrated below:

```python
from mongopyorm import MongoDBConfig

# Set up MongoDB credentials globally
config = MongoDBConfig()
config.set_config(db_name="your_db", username="your_username", password="your_password", cluster_name="your_cluster")

# Now you can use MongoPyORM models with these credentials

```
Once credentials are configured, models will automatically use the provided settings for MongoDB interactions.

## Contributing

Contributions are welcome! Please follow the standard GitHub workflow (fork, feature branch, pull request workflow):

* Fork the repository.
* Create a feature branch (`git checkout -b feature/your-feature`).
* Commit your changes (`git commit -m 'Add your feature'`).
* Push to the branch (`git push origin feature/your-feature`).
* Open a pull request.

## License

This project is licensed under the MIT License.

## Future Enhancements

Support for relationship fields (e.g., ForeignKey-like references).
Query optimizations for large datasets.
More advanced data validation.
Issues

If you encounter any bugs or issues, feel free to open an issue on GitHub.

## Acknowledgments

This project was inspired by the simplicity of traditional ORMs and the power of MongoDB, aiming to bring them together seamlessly.

## Contact

For any inquiries or support, please contact [brannstrom9911@gmail.com].

Feel free to modify this `README.md` to better fit the specific goals or features you want to highlight for your package!