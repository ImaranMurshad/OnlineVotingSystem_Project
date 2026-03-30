from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db.models import Count

from .models import Candidate, Vote
from .forms import CandidateForm
from elections.models import Election


# =========================
# 🔹 ADD CANDIDATE (HOST)
# =========================
@login_required
def add_candidate(request, election_id):
    election = get_object_or_404(Election, id=election_id, host=request.user)

    form = CandidateForm()

    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.election = election
            candidate.save()

            messages.success(request, "Candidate added successfully ✅")
            return redirect('add_candidate', election_id=election.id)

    candidates = Candidate.objects.filter(election=election)

    return render(request, 'voting/add_candidate.html', {
        'form': form,
        'candidates': candidates,
        'election': election
    })


# =========================
# 🔹 VOTER - SEE ELECTIONS
# =========================
@login_required
def voter_elections(request):
    now = timezone.now()

    elections = Election.objects.filter(
        start_date__lte=now,
        end_date__gte=now
    )

    return render(request, 'voting/voter_elections.html', {
        'elections': elections
    })


# =========================
# 🔹 VOTE FUNCTION (CLEAN)
# =========================
@login_required
def vote(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    candidates = Candidate.objects.filter(election=election)

    # 🚫 Prevent multiple voting
    already_voted = Vote.objects.filter(
        election=election,
        user=request.user
    ).exists()

    if already_voted:
        return render(request, 'voting/already_voted.html')

    if request.method == 'POST':
        candidate_id = request.POST.get('candidate')

        if not candidate_id:
            messages.error(request, "Please select a candidate ❌")
            return redirect('vote', election_id=election.id)

        candidate = get_object_or_404(Candidate, id=candidate_id)

        Vote.objects.create(
            election=election,
            candidate=candidate,
            user=request.user   # ✅ FIXED
        )

        return render(request, 'voting/vote_success.html')

    return render(request, 'voting/vote.html', {
        'election': election,
        'candidates': candidates
    })


# =========================
# 🔹 RESULTS (HOST)
# =========================
@login_required
def election_results(request, election_id):
    election = get_object_or_404(Election, id=election_id, host=request.user)

    # 🔥 FIXED HERE
    results = Candidate.objects.filter(election=election).annotate(
        total_votes=Count('votes')   # ✅ MUST BE 'votes'
    ).order_by('-total_votes')

    winner = results.first() if results.exists() else None

    return render(request, 'voting/results.html', {
        'election': election,
        'results': results,
        'winner': winner
    })


# =========================
# 🔹 DELETE CANDIDATE
# =========================
@login_required
def delete_candidate(request, candidate_id):
    candidate = Candidate.objects.filter(
        id=candidate_id,
        election__host=request.user
    ).first()

    if not candidate:
        messages.error(request, "Candidate not found ❌")
        return redirect('host_dashboard')

    election_id = candidate.election.id
    candidate.delete()

    messages.success(request, "Candidate deleted successfully ✅")
    return redirect('add_candidate', election_id=election_id)