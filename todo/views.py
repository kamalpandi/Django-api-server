from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer


@api_view(["GET"])
def get_todos(request):
    todos = Todo.objects.order_by("-date")
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_todo(request):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def remove_todo(request, item_id):
    return Response(
        {'message': 'Deletion is currently disabled.'},
        status=status.HTTP_403_FORBIDDEN
    )
    # try:
    #     todo = Todo.objects.get(id=item_id)
    #     todo.delete()
    #     return Response({"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)
    # except Todo.DoesNotExist:
    #     return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
