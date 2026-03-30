from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from .models import Election
from .forms import ElectionForm


# 🔥 CREATE ELECTION
@login_required
def create_election(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')

        # ✅ Validation
        if not title or not start or not end:
            messages.error(request, "All fields are required")
            return redirect('create_election')

        if start >= end:
            messages.error(request, "End date must be after start date")
            return redirect('create_election')

        # ✅ Save
        Election.objects.create(
            title=title,
            description=description,
            start_date=start,
            end_date=end,
            host=request.user
        )

        messages.success(request, "Election Created Successfully")
        return redirect('my_elections')

    return render(request, 'elections/create_election.html')


# 🔥 MY ELECTIONS (WITH STATUS SUPPORT)
@login_required
def my_elections(request):
    elections = Election.objects.filter(host=request.user)

    return render(request, 'elections/my_elections.html', {
        'elections': elections,
        'now': timezone.now()   # 🔥 for status badges
    })


# 🔥 EDIT ELECTION
@login_required
def edit_election(request, election_id):
    election = get_object_or_404(Election, id=election_id, host=request.user)

    if request.method == 'POST':
        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            form.save()
            messages.success(request, "Election Updated Successfully")
            return redirect('my_elections')
    else:
        form = ElectionForm(instance=election)   # 🔥 THIS LINE FIXES ERROR

    return render(request, 'elections/edit_election.html', {
        'form': form,
        'election': election
    })