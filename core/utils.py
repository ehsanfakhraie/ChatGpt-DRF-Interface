import openai
from authentication.models import User
from core.models import Message
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY


def estimate_token_count(text):
    """Estimate token count for a given text."""
    # OpenAI considers a token to be up to 4 bytes of UTF-8 text.
    # This is a simplification for estimation purposes.
    return max(len(text.encode('utf-8')) // 4, 1)  # Ensure at least 1 token is counted


def calculate_message_token(chat_session):
    """Calculate the total estimated token count for a chat session."""
    total_tokens = 0
    messages = chat_session.messages.all().order_by('created_at')

    for message in messages:
        total_tokens += estimate_token_count(message.text)

    return total_tokens


def create_openai_request_payload(chat_session):
    messages = Message.objects.filter(chat_session=chat_session).order_by('created_at')
    payload_messages = []

    for message in messages:
        payload_messages.append({"role": message.role, "content": message.text})

    return payload_messages


def send_chat_to_openai(chat_session, user):
    messages_payload = create_openai_request_payload(chat_session)

    # Calculate the max tokens we can use for this request, based on the user's remaining tokens
    max_tokens = min(user.tokens, settings.MAX_TOKENS_PER_REQUEST)

    response = openai.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages_payload,
        max_tokens=max_tokens
    )

    # Extract the actual token count used by this completion
    total_token_used = response.usage.total_tokens
    prompt_token_used = response.usage.prompt_tokens
    completion_token_user = response.usage.completion_tokens

    # Assuming the last response from the API is the assistant's latest message
    latest_response = response.choices[0].message.content

    return latest_response, total_token_used, prompt_token_used, completion_token_user
