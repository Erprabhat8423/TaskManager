# Task Management API

## Overview

The Task Management API is a Django-based RESTful API for managing tasks, users, and comments. This API allows for user registration, login, task creation, task management, and comment handling. The API uses token-based authentication and is documented with Swagger.

## Features

- **User Management**: Register new users, login, and receive authentication tokens.
- **Task Management**: Create, retrieve, update, and delete tasks.
- **Task Members**: Add or remove members from tasks.
- **Comments**: Add comments to tasks.
- **Task Status**: Update the status of tasks.
- **Swagger Documentation**: Interactive API documentation using Swagger.

## Technologies Used

- **Django**: Web framework for Python.
- **Django REST Framework**: Toolkit for building Web APIs.
- **DRF-YASG**: Swagger generation tool for Django REST Framework.
- **SQLite**: Default database (can be changed as per requirements).
- **Token Authentication**: For securing endpoints.

## Setup Instructions

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Installation

1. **Clone the Repository**

    ```bash
    git@github.com:Erprabhat8423/TaskManager.git
    https://github.com/Erprabhat8423/TaskManager.git
    cd task-management-api
    ```

2. **Create and Activate Virtual Environment**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply Migrations**

    ```bash
    python manage.py migrate
    ```

5. **Create a Superuser (optional)**

    ```bash
    python manage.py createsuperuser
    username : root
    password: root@123
    ```

6. **Run the Development Server**

    ```bash
    python manage.py runserver
    ```

7. **Access Swagger Documentation**

    Open your browser and navigate to `http://127.0.0.1:8000/swagger/` to interact with the API.
   
7. **Access Redoc Documentation**

    Open your browser and navigate to `http://127.0.0.1:8000/redoc/` to interact with the API.

## Endpoints

### User Management

- **POST /api/register/**: Register a new user.
- **POST /api/login/**: Login and receive an authentication token.

### Task Management

- **POST /api/tasks/**: Create a new task.
- **GET /api/tasks/**: List all tasks.
- **GET /api/tasks/{id}/**: Retrieve a specific task.
- **PUT /api/tasks/{id}/**: Update a specific task.
- **DELETE /api/tasks/{id}/**: Delete a specific task.

### Task Members

- **POST /api/tasks/{id}/members/**: Add a member to a task.
- **DELETE /api/tasks/{id}/members/**: Remove a member from a task.
- **GET /api/tasks/{id}/members/**: List members of a task.

### Comments

- **POST /api/tasks/{task_pk}/comments/**: Add a comment to a task.

### Task Status

- **PATCH /api/tasks/{id}/status/**: Update the status of a task.

## Swagger Documentation

Swagger documentation is available at `/swagger/`. It provides interactive documentation for the API endpoints.

## Redoc Documentation

Swagger documentation is available at `/redoc/`. It provides interactive documentation for the API endpoints.

## Deployment

To deploy the application, you can use platforms like Netlify, PythonAnywhere, or similar. Follow their respective deployment guides to set up your Django project.

## Contributing

Feel free to fork the repository and submit pull requests. Please ensure your changes adhere to the existing code style and include appropriate test coverage.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue on GitHub or contact me via vkc842396@gmail.com.
