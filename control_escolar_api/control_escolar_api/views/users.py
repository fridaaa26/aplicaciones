from django.db.models import *
from django.db import transaction
from control_escolar_api.serializers import UserSerializer
from control_escolar_api.serializers import *
from control_escolar_api.models import *
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import Group

class AdminAll(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        user = request.user
        #TODO: Regresar perfil del administradors
        return Response({})

class AdminView(generics.CreateAPIView):
    #registrar nuevo usuario
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        #Serializar datos del administrador para volverlo de nuevo un json
        user = UserSerializer(data=request.data)
        if user.is_valid():
            #Grab datos del administrador
            role = request.data['rol']
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.data['email']
            password = request.data['password']
            #Validar si el usuario existe
            existing_user = User.objects.filter(email=email).first()

            if existing_user:
                return Response({"message":"Username "+email+", is already taken"},400)

            user = User.objects.create( username = email,
                                        email = email,
                                        first_name = first_name,
                                        last_name = last_name,
                                        is_active = 1)


            user.save()
            user.set_password(password)
            user.save()

            group, created = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
            group.save()

            #Almacenar los datos adicionales del administrador 
            admin = Administradores.objects.create(user=user,
                                                   clave_admin=request.data ["clave_admin"],
                                                   telefono= request.data ["telefono"],
                                                   rfc= request.data ["rfc"].upper(),
                                                   edad= request.data ["edad"],
                                                   ocupacion= request.data ["ocupacion"])
            return Response ({"Admin creado con el ID: ": admin.id}, 201)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
