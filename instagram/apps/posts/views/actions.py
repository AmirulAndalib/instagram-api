# Python standard library
from typing import Any

# Django Framework
from django.db.models import Model
from django.db.models import QuerySet

# Django REST Framework
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Instagram models
from instagram.apps.posts.models import Post
from instagram.apps.posts.models import Like
from instagram.apps.posts.models import Comment
# Instagram serializers
from instagram.apps.posts.serializers import CommentDetailSerializer


class ActionsMixin(APIView):

    def get_queryset(self, klass: Model, *args: tuple[Any], **kwargs: dict[str, Any]) -> QuerySet:
        if args or kwargs:
            return klass.objects.filter(*args, **kwargs)

        return klass.objects.all()


class LikeAPIView(ActionsMixin):

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        post = self.get_queryset(Post, url=kwargs['url']).first()
        if post:
            Like.objects.create(user=request.user, post=post)

            return Response(
                data={
                    'message': f'Like added to @{post.author.username} post'
                },
                status=status.HTTP_201_CREATED
            )

        return Response({ 'info': 'Post not found' }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        post = self.get_queryset(Post, url=kwargs['url']).first()
        like = self.get_queryset(Like, id=kwargs['id'])

        if post and like:
            like.delete()

            return Response(
                data={ 'message': f'Like removed from {post.author.username} post' },
                status=status.HTTP_200_OK
            )

        return Response({ 'info': 'Post not found' }, status=status.HTTP_404_NOT_FOUND)


class CommentAPIView(ActionsMixin):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, url: str = None, id: int = None, **kwargs: dict[str, Any]) -> Response:
        serializer_class = CommentDetailSerializer

        if id:
            post = self.get_queryset(Post, url=url).first()
            comment = self.get_queryset(Comment, post=post).first()
            serializer = serializer_class(instance=comment)

            return Response(serializer.data, status=status.HTTP_200_OK)

        post = self.get_queryset(Post, url=url).first()
        comments = self.get_queryset(Comment, post=post)
        serializer = serializer_class(comments, many=True)

        return Response({ 'message': 'Comments list', 'comments': serializer.data })

    def post(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        data = request.data
        post = self.get_queryset(Post, url=kwargs['url']).first()

        if post:
            Comment.objects.create(author=request.user, post=post, **data)

            return Response(
                data={ 'message': f'Comment added to @{post.author.username} post' },
                status=status.HTTP_201_CREATED
            )

        return Response(
            data={ 'info': 'Post not found' },
            status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        post = self.get_queryset(Post, url=kwargs['url']).first()
        comment = self.get_queryset(Comment, id=kwargs['id'])

        if post and comment:
            comment.delete()

            return Response(
                data={ 'message': f'Comment removed from @{post.author.username} post' },
                status=status.HTTP_200_OK
            )

        return Response(
            data={ 'info': 'Post or comment not found' },
            status=status.HTTP_404_NOT_FOUND
        )