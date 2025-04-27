# tribes/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from django.conf import settings
from openai import OpenAI
from .models import People, Favorite, Comment
from .serializers import PeopleSerializer, UserRegistrationSerializer, FavoriteSerializer, CommentSerializer, UserProfileSerializer

class PeopleListView(generics.ListAPIView):
    queryset = People.objects.all()
    serializer_class = PeopleSerializer

class PeopleDetailView(generics.RetrieveUpdateAPIView):  # Меняем на RetrieveUpdateAPIView
    queryset = People.objects.all()
    serializer_class = PeopleSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]  # GET для всех, PUT только для авторизованных

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class FavoriteListView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        people_slug = self.request.data.get('people_slug')
        try:
            people = People.objects.get(slug=people_slug)
        except People.DoesNotExist:
            return Response({"error": "Culture not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer.save(user=self.request.user, people=people)

class FavoriteDeleteView(generics.DestroyAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        people_slug = self.kwargs['slug']
        return Comment.objects.filter(people__slug=people_slug)

    def perform_create(self, serializer):
        people_slug = self.kwargs['slug']
        try:
            people = People.objects.get(slug=people_slug)
        except People.DoesNotExist:
            return Response({"error": "Culture not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer.save(user=self.request.user, people=people)

class ChatView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, slug):
        try:
            people = People.objects.get(slug=slug)
        except People.DoesNotExist:
            return Response({"error": "People not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": f"Welcome to the {people.name} chat! Send a POST request with a message to start chatting."})

    def post(self, request, slug):
        message = request.data.get('message')
        if not message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            people = People.objects.get(slug=slug)
        except People.DoesNotExist:
            return Response({"error": "People not found"}, status=status.HTTP_404_NOT_FOUND)

        if not settings.OPENAI_API_KEY:
            return Response({"error": "OpenAI API key is missing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Act as {people.name}. Reply shortly about your culture. Постарайся отвечать кратко и интересно до 2-3 предложений."},
                    {"role": "user", "content": message}
                ],
                max_tokens=170,
                temperature=0.7
            )
            return Response({"response": response.choices[0].message.content.strip()})
        except Exception as e:
            return Response({"error": f"Failed to get response from AI: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response(
                {"error": "Both old_password and new_password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(old_password):
            return Response(
                {"error": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"message": "Password updated successfully"},
            status=status.HTTP_200_OK
        )