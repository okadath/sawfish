DJOSER!!!!!

default=
null blank  unique

max_length=149

ForeignKey
ManyToManyField
OneToOneField

models.CharField(max_length=149) 
models.TextField(blank=True, null=True)
models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
models.FileField(upload_to='pictures/', blank=True, null=True)
models.ForeignKey(Language, related_name='Language_speaker_foreign_data', on_delete=models.CASCADE, default=1)
models.BooleanField(default=False)

import datetime
models.DateTimeField(default=datetime.datetime.now)



# ==========profile
from django.contrib.auth.models import User
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	picture = models.FileField(upload_to='pics/', blank=True, null=True)
	def __str__(self):
		return self.user.username


# ====================ejemplo de modelo

from django.db import models

class Car(models.Model):
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.CASCADE,
    )
    # ...

class Manufacturer(models.Model):
    # ...
    pass

# =======================signals

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from user_account.models import Profile

from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db import transaction



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	"""
	una señal que crea un profile automaticamente al momento de registrar un nuevo usuario
	esto permitiria la edicion de un modulo de usuario para la compra de codigos
	como en las redes sociales, falto la señal para eliminar un usuario cuando se elimina su profile
	(la señal inversa a este)
	"""
	if created:
		Profile.objects.create(user=instance)
 


# =======================admin


from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.sessions.models import Session

admin.site.register(Profile)
admin.site.register(Year)
admin.site.register(Region)
admin.site.register(LoggedInUser)
admin.site.register(Session)
# admin.site.register(LocalSite)
# admin.site.register(Organization)
# admin.site.register(Season)
# admin.site.register(License)
# admin.site.register(Order)


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAdmin(BaseAdmin, ImportExportModelAdmin):
    resource_class = UserResource


@admin.register(Language)
class LanguageAdmin(ImportExportModelAdmin):
    list_display = ['lang', 'lang_code']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Code)
class CodeAdmin(ImportExportModelAdmin):
    list_display = ['code']


@admin.register(User_Code)
class UserCodeAdmin(ImportExportModelAdmin):
	pass 


# =============================apps

from django.apps import AppConfig
# from paypal.standard.ipn.signals import valid_ipn_received#remove?


class UserAccountConfig(AppConfig):
    name = 'user_account'
    def ready(self):
    	# señal para la creacion del profile automaticamente 
    	# al crear un usuario, remove?
        import user_account.utils.signals


# =============================serializers

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = '__all__'


class User_CodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=True)
    code = serializers.CharField(source='code.code', required=True)

    class Meta:
        model = User_Code
        fields = ('id', 'username', 'code')
        read_only_fields = ('username', 'code')


# ================vistas, usar las 4 vistas del apiview,
# no se si aqui debo usar la vista sencilla con un id y las bsuquedas e insertarla al router
# o hacerlas individuales e insertarlas a mano
# si es personalizada le pondre los metodos de apiview



# =================================urls

from django.urls import include, path
from rest_framework.routers import SimpleRouter
from user_account.views.views_rest import LanguageList,YearList,RegionList,UserView
from user_account.views.views_rest import *
# remove rest?

router=SimpleRouter()
router.register('GET/lang',LanguageList)#,base_name='lang')
# router.register('GET/organization',OrganizationList)#,base_name='organization')
# router.register('GET/localsite',LocalSiteList)#,base_name='localsite')
router.register('GET/year', YearList)
# router.register('GET/licence', LicenseList)
# router.register('GET/season', SeasonList)
router.register('GET/region', RegionList)
# router.register('', UserView)


urlpatterns=router.urls


# from rest_framework.routers import DefaultRouter

urlpatterns = urlpatterns+[
path("<str:username>",UserView.as_view(),name="EditUsers"), 
    #gets all user profiles and create a new profile
    path("GET/profile/",ProfileListView.as_view(),name="all-profiles"),
    # path("POST/profile/",ProfileCreateView.as_view(),name="all-profiles"),
    path("GET/profile/<str:user__username>/",ProfileRetriveView.as_view(),name="profile"),
    path("PUT/profile/<str:user__username>/",ProfileUpdateView.as_view(),name="profile"),
    # path("DELETE/profile/<slug:user__username>/",ProfileDestroyView.as_view(),name="profile"),
    # path("GET/profile/<int:pk>/",ProfileRetriveView.as_view(),name="profile"),
]