from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.conf import settings

from myapp.modules import RftController

# Isso aqui vai ser meu controller RftController vai passar para cá
# Create your views here.
class app(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		print(request)
		print(type(request))

		data = dict(request.data)
		action = data.pop('action')

		response = RftController.run(data, action)
		return Response(response, status=status.HTTP_200_OK)