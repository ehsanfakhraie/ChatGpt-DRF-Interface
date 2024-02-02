# Django Restful Api Interface for Chat-Gpt

This Django project implements a chat application that integrates with OpenAI's GPT models to respond. It allows users to create chat sessions, send messages, and receive replies from an AI assistant. The application also tracks user tokens to manage and limit the usage of the OpenAI API.

## Features

- User authentication and registration with Lincense Code Logic.
- Chat sessions management.
- Sending and receiving messages within a chat session.
- Integration with OpenAI's Api for AI-generated responses.
- Token system for usage management and billing.
- Admin interface for managing users, chat sessions, and messages.

## Prerequisites

- Python 3.8 or higher
- Django 3.2 or higher
- Django REST Framework
- An OpenAI API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ehsanfakhraie/ChatGpt-DRF-Interface
cd ChatGpt-DRF-Interface
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:

   - Set `OPENAI_API_KEY='your_openai_api_key_here'` in `settings.py`.

4. Run migrations to create the database schema:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser account:

```bash
python manage.py createsuperuser
```

6. Start the development server:

```bash
python manage.py runserver
```

## Usage

- Visit `http://localhost:8000/admin/` to access the Django admin interface.
- Use the API endpoints to create chat sessions, send messages, and interact with the AI:
  - `/api/core/chat_sessions/` to manage chat sessions.
  - `/api/core/messages/` to send and receive messages.

## Configuration
- Set your openai API token in `settings.py`
- Customize max token count and OpenAI model settings in `settings.py`.
- Adjust the token estimation logic in `utils.py` based on your needs.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
