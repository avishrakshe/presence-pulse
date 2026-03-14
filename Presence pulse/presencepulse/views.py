from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import mysql.connector
import json
from . import db

# Initialize DB tables on startup
# db.init_db()  # Commented out: blocks startup if MySQL is not running yet. Call manually or on first request.

def landing(request):
    return render(request, 'landing.html')

def dashboard(request):
    return render(request, 'dashboard.html', get_user_context(request))

def sessions(request):
    return render(request, 'sessions.html', get_user_context(request))

def nudges(request):
    return render(request, 'nudges.html', get_user_context(request))

def insights(request):
    return render(request, 'insights.html', get_user_context(request))

def settings_page(request):
    return render(request, 'settings.html', get_user_context(request))

def get_user_context(request):
    """Return a context dict with logged-in user info from session."""
    first_name = request.session.get('first_name', '')
    last_name  = request.session.get('last_name', '')
    email      = request.session.get('user_email', '')
    full_name  = f"{first_name} {last_name}".strip() or 'User'
    initials   = (first_name[:1] + last_name[:1]).upper() or 'U'
    return {
        'user_first_name': first_name,
        'user_last_name':  last_name,
        'user_full_name':  full_name,
        'user_email':      email,
        'user_initials':   initials,
    }


def login(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        
        conn = db.get_connection()
        if not conn:
            context['error'] = "Database connection error."
            return render(request, 'login.html', context)

        # Quick dev bypass
        if email == "abc@123" and password == "123":
            request.session['first_name'] = 'Demo'
            request.session['last_name']  = 'User'
            request.session['user_email'] = 'demo@example.com'
            return redirect('dashboard')
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if user and check_password(password, user['password_hash']):
                request.session['first_name'] = user.get('first_name', '')
                request.session['last_name']  = user.get('last_name', '')
                request.session['user_email'] = user.get('email', '')
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
            # Store email in session for onboarding flow
            request.session['onboarding_email'] = email
            return redirect('daily_schedule')
        except mysql.connector.IntegrityError:
            context['error'] = "An account with this email already exists."
        except Exception as e:
            context['error'] = f"Error creating account: {e}"
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()
            
    return render(request, 'signup.html', context)


def daily_schedule(request):
    context = {}
    if request.method == 'POST':
        email = request.session.get('onboarding_email', '')
        wake_time = request.POST.get('wake_time')
        work_start = request.POST.get('work_start')
        work_end = request.POST.get('work_end')
        lunch_time = request.POST.get('lunch_time')
        dinner_time = request.POST.get('dinner_time')
        bed_time = request.POST.get('bed_time')
        exercise_time = request.POST.get('exercise_time') or None
        no_phone_meals = int(request.POST.get('no_phone_meals', 0))
        no_phone_bedtime = int(request.POST.get('no_phone_bedtime', 0))
        no_phone_exercise = int(request.POST.get('no_phone_exercise', 0))

        conn = db.get_connection()
        if not conn:
            context['error'] = "Database connection error."
            return render(request, 'daily_schedule.html', context)

        try:
            cursor = conn.cursor()
            query = """
                UPDATE users SET
                    wake_time = %s, work_start = %s, work_end = %s,
                    lunch_time = %s, dinner_time = %s, bed_time = %s,
                    exercise_time = %s, no_phone_meals = %s,
                    no_phone_bedtime = %s, no_phone_exercise = %s
                WHERE email = %s
            """
            cursor.execute(query, (wake_time, work_start, work_end, lunch_time, dinner_time, bed_time, exercise_time, no_phone_meals, no_phone_bedtime, no_phone_exercise, email))
            conn.commit()
            return redirect('social_media_goals')
        except Exception as e:
            context['error'] = f"Error saving schedule: {e}"
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()

    return render(request, 'daily_schedule.html', context)


def social_media_goals(request):
    context = {}
    if request.method == 'POST':
        email = request.session.get('onboarding_email', '')
        notify_on_exceed = int(request.POST.get('notify_on_exceed', 0))
        weekend_relaxed = int(request.POST.get('weekend_relaxed', 0))

        # Get each platform's limit
        sm_instagram = int(request.POST.get('instagram', 0))
        sm_twitter = int(request.POST.get('twitter', 0))
        sm_facebook = int(request.POST.get('facebook', 0))
        sm_tiktok = int(request.POST.get('tiktok', 0))
        sm_youtube = int(request.POST.get('youtube', 0))
        sm_whatsapp = int(request.POST.get('whatsapp', 0))
        sm_snapchat = int(request.POST.get('snapchat', 0))
        sm_reddit = int(request.POST.get('reddit', 0))

        conn = db.get_connection()
        if not conn:
            context['error'] = "Database connection error."
            return render(request, 'social_media_goals.html', context)

        try:
            cursor = conn.cursor()
            query = """
                UPDATE users SET
                    sm_instagram = %s, sm_twitter = %s, sm_facebook = %s,
                    sm_tiktok = %s, sm_youtube = %s, sm_whatsapp = %s,
                    sm_snapchat = %s, sm_reddit = %s,
                    notify_on_exceed = %s, weekend_relaxed = %s
                WHERE email = %s
            """
            cursor.execute(query, (sm_instagram, sm_twitter, sm_facebook, sm_tiktok, sm_youtube, sm_whatsapp, sm_snapchat, sm_reddit, notify_on_exceed, weekend_relaxed, email))
            conn.commit()
            # Clear onboarding session
            if 'onboarding_email' in request.session:
                del request.session['onboarding_email']
            return redirect('dashboard')
        except Exception as e:
            context['error'] = f"Error saving goals: {e}"
        finally:
            if 'cursor' in locals(): cursor.close()
            conn.close()

    return render(request, 'social_media_goals.html', context)


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


@csrf_exempt
def respond_challenge(request):
    """API endpoint for accepting/rejecting challenge nudges."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    email = request.session.get('onboarding_email', '')
    challenge_name = data.get('challenge_name', '')
    trigger = data.get('trigger', '')
    action = data.get('action', '')
    points_change = int(data.get('points_change', 0))

    if action not in ('accept', 'reject'):
        return JsonResponse({'error': 'Invalid action'}, status=400)

    conn = db.get_connection()
    if not conn:
        return JsonResponse({'error': 'Database error'}, status=500)

    try:
        cursor = conn.cursor()

        # Log the challenge response
        cursor.execute("""
            INSERT INTO challenge_responses (user_email, challenge_name, trigger_reason, action, points_change)
            VALUES (%s, %s, %s, %s, %s)
        """, (email, challenge_name, trigger, action, points_change))

        # Update user's presence points
        if email:
            cursor.execute("""
                UPDATE users SET presence_points = presence_points + %s WHERE email = %s
            """, (points_change, email))

        conn.commit()
        return JsonResponse({'status': 'ok', 'points_change': points_change})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        if 'cursor' in locals(): cursor.close()
        conn.close()