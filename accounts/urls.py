from django.urls import path
from .views import (CheckUserVerifiedRegisterdViewSet, UserCreateAPIView, SetCodeToZero, ChangePhoneNumber,
                    UserFirebaseToken, SendNotifications, UpdateUserProfile, UserPermissions, WhoCanEdit,
                    ResendConfirmationCode)

urlpatterns = [
    path('checkifuserisregisterdandverified/', CheckUserVerifiedRegisterdViewSet.as_view()),
    path('registration/', UserCreateAPIView.as_view()),
    path('codeset/', SetCodeToZero.as_view()),
    path('resendconfirmationcode/', ResendConfirmationCode.as_view()),
    path('changephonenumber/', ChangePhoneNumber.as_view()),
    path('userfirebasetoken/', UserFirebaseToken.as_view()),
    path('updateuserprofile/', UpdateUserProfile.as_view()),
    path('permissions/', UserPermissions.as_view()),
    path('sendnotification/', SendNotifications.as_view()),
    path('whocanedit/', WhoCanEdit.as_view()), ]
