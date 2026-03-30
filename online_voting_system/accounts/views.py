from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from .forms import RegisterForm
from .models import User
from elections.models import Election


# =========================
# 🔹 HOME
# =========================
def home(request):
    return render(request, 'accounts/home.html')


# =========================
# 🔹 REGISTER HOST
# =========================
def register_host(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists ❌")
                return redirect(request.path)

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists ❌")
                return redirect(request.path)

            user = form.save(commit=False)
            user.role = 'host'
            user.status = 1  # ✅ auto approve host
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request, "Host registered successfully ✅")
            return redirect('login')

    return render(request, 'accounts/register_host.html', {'form': form})


# =========================
# 🔹 REGISTER VOTER
# =========================
def register_voter(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists ❌")
                return redirect(request.path)

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists ❌")
                return redirect(request.path)

            user = form.save(commit=False)
            user.role = 'voter'
            user.status = 0  # ⏳ pending

            # 🔥 assign FIRST host (can improve later)
            host = User.objects.filter(role='host').first()

            if not host:
                messages.error(request, "No host available ❌")
                return redirect('register_voter')

            user.host = host
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request, "Voter registered. Wait for approval ✅")
            return redirect('login')

    return render(request, 'accounts/register_voter.html', {'form': form})


# =========================
# 🔹 LOGIN
# =========================
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.status == 1:
                login(request, user)

                if user.role == 'admin':
                    return redirect('/admin/')
                elif user.role == 'host':
                    return redirect('host_dashboard')
                else:
                    return redirect('voter_dashboard')
            else:
                messages.error(request, "Account not approved ❌")
        else:
            messages.error(request, "Invalid credentials ❌")

    return render(request, 'accounts/login.html')


# =========================
# 🔹 LOGOUT
# =========================
def user_logout(request):
    logout(request)
    return redirect('login')


# =========================
# 🔹 HOST DASHBOARD
# =========================
@login_required
def host_dashboard(request):
    now = timezone.now()

    total = Election.objects.filter(host=request.user).count()

    active = Election.objects.filter(
        host=request.user,
        start_date__lte=now,
        end_date__gte=now
    ).count()

    pending = User.objects.filter(
        role='voter',
        status=0,
        host=request.user
    ).count()

    return render(request, 'accounts/host_dashboard.html', {
        'total': total,
        'active': active,
        'pending': pending
    })


# =========================
# 🔹 VOTER DASHBOARD
# =========================
@login_required
def voter_dashboard(request):
    now = timezone.now()

    active_elections = Election.objects.filter(
        start_date__lte=now,
        end_date__gte=now
    ).count()

    return render(request, 'accounts/voter_dashboard.html', {
        'active_elections': active_elections
    })


# =========================
# 🔹 ADMIN APPROVAL
# =========================
@staff_member_required
def approve_users(request):
    voters = User.objects.filter(status=0, role='voter')
    return render(request, 'accounts/approve_users.html', {'voters': voters})


@staff_member_required
def approve_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 1
    user.save()

    messages.success(request, "User Approved ✅")
    return redirect('approve_users')


@staff_member_required
def reject_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.status = 2
    user.save()

    messages.error(request, "User Rejected ❌")
    return redirect('approve_users')


# =========================
# 🔹 HOST APPROVE VOTERS
# =========================
@login_required
def host_approve_voters(request):
    voters = User.objects.filter(
        role='voter',
        status=0,
        host=request.user
    )

    return render(request, 'accounts/host_approve.html', {'voters': voters})


@login_required
def approve_voter(request, user_id):
    voter = get_object_or_404(User, id=user_id, role='voter', host=request.user)

    voter.status = 1
    voter.save()

    messages.success(request, "Voter Approved ✅")
    return redirect('host_approve_voters')


@login_required
def reject_voter(request, user_id):
    voter = get_object_or_404(User, id=user_id, role='voter', host=request.user)

    voter.status = 2
    voter.save()

    messages.error(request, "Voter Rejected ❌")
    return redirect('host_approve_voters')


# =========================
# 🔹 STATIC PAGES
# =========================
def about(request):
    return render(request, 'accounts/about.html')


def contact(request):
    return render(request, 'accounts/contact.html')


# =========================
# 🔹 VOTER ELECTION LIST
# =========================
@login_required
def voter_elections(request):
    now = timezone.now()

    elections = Election.objects.filter(
        start_date__lte=now,
        end_date__gte=now
    )

    return render(request, 'accounts/voter_elections.html', {
        'elections': elections
    })