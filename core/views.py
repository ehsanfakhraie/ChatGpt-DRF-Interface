from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from authentication.models import User
from .models import ChatSession, Message  # Ensure User is imported
from .serializers import ChatSessionSerializer, MessageSerializer
from .utils import *  # Updated to use the role field and handle tokens


class ChatSessionViewSet(viewsets.ModelViewSet):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageViewSet(viewsets.ViewSet):
    def create(self, request):
        chat_session_id = request.data.get('chat_session_id')
        text = request.data.get('text')
        chat_session = get_object_or_404(ChatSession, id=chat_session_id, user=request.user)

        user = request.user

        if not chat_session.messages.exists():
            # Properly create the initial system message for new chat sessions
            Message.objects.create(
                chat_session=chat_session,
                text=settings.CHAT_INSTRUCTIONS,
                role="system"
            )

        # Save the user's message
        user_message = Message.objects.create(
            chat_session=chat_session,
            text=text,
            role="user",
        )

        # Before sending the message to OpenAI, ensure the user has enough tokens
        estimated_tokens = calculate_message_token(
            chat_session)

        user_message.estimated_tokens = estimated_tokens
        user_message.save()

        if user.tokens < estimated_tokens:
            return Response({"error": "Not enough tokens."}, status=status.HTTP_402_PAYMENT_REQUIRED)

        # Retrieve and send the entire chat session to OpenAI, then get the response and actual tokens used
        response_text, total_tokens, prompt_tokens, completion_tokens = send_chat_to_openai(chat_session, request.user)

        # Deduct tokens based on actual usage
        user.charge_tokens(total_tokens)

        # Save OpenAI's response
        ai_message = Message.objects.create(
            chat_session=chat_session,
            text=response_text,
            role="assistant",
            total_tokens=total_tokens,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens
        )

        return Response({
            "user_message": MessageSerializer(user_message).data,
            "ai_message": MessageSerializer(ai_message).data,
            "tokens_remaining": request.user.tokens
        }, status=status.HTTP_201_CREATED)
