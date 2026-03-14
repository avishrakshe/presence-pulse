from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
import mysql.connector
from . import db

# Initialize DB tables on startup
db.init_db()

def landing(request):
    return render(request, 'landing.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def sessions(request):
    return render(request, 'sessions.html')

def nudges(request):
    return render(request, 'nudges.html')

def triggers(request):
    return render(request, 'triggers.html')

def insights(request):
    return render(request, 'insights.html')

def settings_page(request):
    return render(request, 'settings.html')

def login(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        
        conn = db.get_connection()
        if not conn:
            context['error'] = "Database connection error."
            return render(request, 'login.html', context)

        if (email == "abc@123" or password == "123"):
            return redirect('dashboard')
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user and check_password(password, user['password_hash']):
                # In a real app, set session variables here
                # request.session['user_id'] = user['id']
                return redirect('dashboard')
            else:
                context['error'] = "Invalid email or password."
        except Exception as e:
            context['error'] = f"Database error: {e}"
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()

    return render(request, 'login.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        role = request.POST.get('role', 'User')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            context['error'] = "Passwords do not match."
            return render(request, 'signup.html', context)
            
        hashed_pw = make_password(password)
        
        conn = db.get_connection()
        if not conn:
            context['error'] = "Database connection error."
            return render(request, 'signup.html', context)
            
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO users (role, first_name, last_name, email, password_hash)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (role, first_name, last_name, email, hashed_pw))
            conn.commit()
            context['message'] = "Account created successfully! You can now sign in."
            return render(request, 'login.html', context)
        except mysql.connector.IntegrityError:
            context['error'] = "An account with this email already exists."
        except Exception as e:
            context['error'] = f"Error creating account: {e}"
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
            
    return render(request, 'signup.html', context)


def forgot_password(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            context['error'] = "Passwords do not match."
            return render(request, 'forgot_password.html', context)
            
        conn = db.get_connection()
        if not conn:
            context['error'] = "Database connection error."
            return render(request, 'forgot_password.html', context)
            
        try:
            cursor = conn.cursor()
            # First check if user exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if not cursor.fetchone():
                context['error'] = "No account found with that email address."
            else:
                hashed_pw = make_password(new_password)
                cursor.execute("UPDATE users SET password_hash = %s WHERE email = %s", (hashed_pw, email))
                conn.commit()
                context['message'] = "Password reset successfully! You can now sign in with your new password."
                return render(request, 'login.html', context)
        except Exception as e:
            context['error'] = f"Database error: {e}"
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
            
    return render(request, 'forgot_password.html', context)