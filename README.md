# Hidden Gem

[![Build Status](https://travis-ci.org/your-username/your-repo.svg?branch=master)](https://travis-ci.org/your-username/your-repo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description

This backend application serves API for the hiddenGem web where user can find reviews of awesome places anywhere in the world as well as submit their reviews/comments about those places.

## Features

- See user list
- See user detail by id
- Add new user
- Update user data
- Delete user
- See reviews
- Get recommendations ?
- ...

## Technologies Used

- Flask
- Python
- [Other dependencies]


## Configuration

Create an env file and export it
```bash
FLASK_APP=main.py
DB_HOST=localhost
DB_DATABASE=your_database
DB_USERNAME=your_database_username
DB_PASSWORD=your_database_password
```

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/project-zusammen/hidden-gem-backend.git
    ```

2. Create virtual environment:
    ```bash
    python -m venv venv
    ```

3. Activate virtual environment:
    ```bash
    source venv/bin/activate
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Initializes Flask-Migrate within your Flask application.
    ```bash
    flask db init
    ```
6. Creates an automatic migration script
    ```bash
    flask db migrate -m "user table"
    ```
    The -m flag allows you to add a message or description for this migration. And make sure to run this command every time you add or modify the model database

7. Applies the generated migration script to the database.
    ```bash
    flask db upgrade
    ```

6. Run the application
    ```bash
    flask run
    ```

6. Run the tests:
    ```bash
    besok dah..
    ```

## Usage

1. Add New User (Method = POST): 
```
curl --location 'http://127.0.0.1:5000/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username" : "ikan tenggiri",
    "email": "tenggiri@gmail.com",
    "password" : "tenggiri123" 

}'
```

Result: 
```json
{
    "message": "Successfully create user!"
}
```

2. Get User Lists (Method = GET): 
```
curl --location 'http://127.0.0.1:5000/users'
```

Result: 
```json
{
    "data": [
        {
            "email": "tenggiri@gmail.com",
            "id": 1,
            "role": "user",
            "username": "ikan tenggiri"
        }
    ],
    "message": "Success Get User lists"
}
```

## Contributing

If you'd like to contribute to the project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Mention any external libraries, resources, or inspiration you used.

## Contact

- Your Name
- Your Email
- Any other contact information you'd like to provide.

