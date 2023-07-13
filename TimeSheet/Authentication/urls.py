from django.urls import path
from Authentication import views

urlpatterns = [
    path('register/', views.sign_up, name='register'),
    path('login/',views.login_n, name = 'login'),
    path('logout', views.logout_n, name='logout'),
    path('getUser',views.getUser, name='getuser'),
    path('changePassword',views.changePassword, name='newPassword'),
    path('updatePassword',views.updatePassword,name="updatePassword"),
    path('resetpassword',views.resetPassword, name='resetPassword'),
    path('settings/',views.userSetting,name="settings"),
    path('activate/',views.activateUser,name="active"),
    path('superuser',views.adminUser,name="admin"),
    path('teams/<teamid>',views.getTeams,name='teams'),
    path('searchUsers',views.searchUser,name="searchuser"),
    path('addUsersTeam',views.addToTeams,name='addtoteam'),
    path('removefromTeam',views.removeFromTeam,name='removeFromTeam'),
]