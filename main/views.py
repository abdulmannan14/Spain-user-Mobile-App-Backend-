from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models as main_models
from . import serializers as main_serializers
from django.http import Http404
from rest_framework.permissions import IsAuthenticated, AllowAny
import csv
from io import StringIO


class UserDetails(APIView):
    permission_classes = (AllowAny,)
    serializer_class = main_serializers.GetCSVAndCreateUserDetailSerializer
    put_serializer_class = main_serializers.UpdateUserCardImageSerializer

    def get(self, request, format=None):
        user_details = main_models.UserDetails.objects.filter(card__isnull=False)
        serializer = main_serializers.UserDetailSerializer(user_details, many=True)
        return Response(serializer.data)

    # This api is for getting the CSV file and Creating the UserDetail Objects
    @csrf_exempt
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = request.FILES['csv_file']
        file_data = file.read().decode('utf-8')
        data_to_send = []
        # read Csv File and save the data in the UserDetail Model
        if file:
            csv_file = StringIO(file_data)
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                obj = main_models.UserDetails.objects.create(
                    name=row['Nombre'],
                    surname=row['Apellidos'],
                    licence=row['Licencia'],
                    dni_nie=row['DNI/NIE'],
                    expedition_date=row['Fecha Expedici¢n'],
                    expiration_date=row['Fecha Vencimiento'],
                    graduated_in=row['Titulado en'],
                    # image=row['Imagen']
                )
                data = {
                    "id": obj.id,
                    "name": row['Nombre'],
                    "surname": row['Apellidos'],
                    "licence": row['Licencia'],
                    "dni_nie": row['DNI/NIE'],
                    "expedition_date": row['Fecha Expedici¢n'],
                    "expiration_date": row['Fecha Vencimiento'],
                    "graduated_in": row['Titulado en'],
                    # "image":row['Imagen']

                }
                data_to_send.append(data)
            return Response({"message": "Data Saved Successfully", "data": data_to_send},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        serializer = self.put_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.data.get('id') or not request.data.get('card'):
            return Response({"message": "Please Provide the ID and Card Image"},
                            status=status.HTTP_400_BAD_REQUEST)
        user_id = request.data.get('id')
        user = main_models.UserDetails.objects.get(id=user_id)
        user.card = request.data.get('card')
        user.save()
        return Response({"message": "Card Image Updated Successfully"}, status=status.HTTP_200_OK)


class AllDone(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        import telnyx
        from django.conf import settings
        user_details = main_models.UserDetails.objects.filter(message_sent=False)
        telnyx.api_key = settings.TELNYX_API_KEY
        telnyx_phone_number = settings.TELNYX_PHONE_NUMBER
        if not telnyx_phone_number and not settings.TELNYX_API_KEY:
            return Response({"message": "Telnyx API Key and Phone Number is not set on Backend"},
                            status=status.HTTP_400_BAD_REQUEST)
        for user in user_details:
            telnyx.Message.create(
                from_=telnyx_phone_number,
                to=user.phone_number,  # Assuming users have a phone_number field
                text="Hello! Your card is ready for download. Please visit the Mobile App to download the card."
            )
            user.message_sent = True
            user.save()
        return Response({"message": "Messages Sent Successfully"}, status=status.HTTP_200_OK)
