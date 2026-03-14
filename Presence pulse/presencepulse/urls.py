from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('landing.html', views.landing, name='landing-file'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard.html', views.dashboard, name='dashboard-file'),
    path('sessions', views.sessions, name='sessions'),
    path('sessions.html', views.sessions, name='sessions-file'),
    path('nudges', views.nudges, name='nudges'),
    path('nudges.html', views.nudges, name='nudges-file'),
    path('triggers', views.triggers, name='triggers'),
    path('triggers.html', views.triggers, name='triggers-file'),
    path('insights', views.insights, name='insights'),
    path('insights.html', views.insights, name='insights-file'),
    path('settings', views.settings_page, name='settings'),
    path('settings.html', views.settings_page, name='settings-file'),
    path('login', views.login, name='login'),
    path('login.html', views.login, name='login-file'),
    path('signup', views.signup, name='signup'),
    path('signup.html', views.signup, name='signup-file'),
    path('forgot-password', views.forgot_password, name='forgot_password'),
    path('forgot_password.html', views.forgot_password, name='forgot_password-file'),
]

# Serve static files (CSS, JS) in development
if settings.DEBUG:
    urlpatterns += static('/', document_root=settings.BASE_DIR)
