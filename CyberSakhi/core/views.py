from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, IncidentReportForm, SafetyChecklistForm
from .models import IncidentReport, AwarenessArticle, SavedArticle, SafetyChecklist
from .detector import analyse_text

def home(request):
    return render(request, "core/home.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your CyberSakhi account is ready.")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "core/register.html", {"form": form})

@login_required
def dashboard(request):
    reports = IncidentReport.objects.filter(user=request.user)
    return render(request, "core/dashboard.html", {
        "reports": reports[:5],
        "total": reports.count(),
        "open_count": reports.exclude(status="closed").count(),
        "articles_count": AwarenessArticle.objects.count(),
    })

def detector(request):
    result = None
    submitted = ""
    if request.method == "POST":
        submitted = request.POST.get("content", "")[:5000]
        result = analyse_text(submitted)
    return render(request, "core/detector.html", {"result": result, "submitted": submitted})

@login_required
def report_create(request):
    if request.method == "POST":
        form = IncidentReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.save()
            messages.success(request, f"Report submitted. Your reference ID is {report.reference_id}.")
            return redirect("report_detail", pk=report.pk)
    else:
        form = IncidentReportForm()
    return render(request, "core/report_form.html", {"form": form})

@login_required
def report_detail(request, pk):
    report = get_object_or_404(IncidentReport, pk=pk, user=request.user)
    return render(request, "core/report_detail.html", {"report": report})

def awareness(request):
    query = request.GET.get("q", "").strip()
    articles = AwarenessArticle.objects.all()
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(category__icontains=query) | Q(summary__icontains=query))
    return render(request, "core/awareness.html", {"articles": articles, "query": query})

def article_detail(request, pk):
    article = get_object_or_404(AwarenessArticle, pk=pk)
    return render(request, "core/article_detail.html", {"article": article})

QUIZ = [
    {"q": "Someone asks you to share an OTP to receive a refund. What should you do?",
     "choices": ["Share it quickly", "Never share it; verify through the official app", "Post it in a group"], "answer": 1,
     "why": "An OTP is private. Legitimate support should not ask you to disclose it."},
    {"q": "A message says your bank account will be blocked unless you click a link. Best response?",
     "choices": ["Click immediately", "Forward it to everyone", "Open the bank's official app or call its verified number"], "answer": 2,
     "why": "Urgency is a common pressure tactic. Verify independently."},
    {"q": "What is safer when checking a website?",
     "choices": ["Trust its logo", "Type the known official address yourself", "Trust any shortened link"], "answer": 1,
     "why": "Logos can be copied. Use a known official address."},
    {"q": "A recruiter asks you to pay a fee before giving a job. What is a warning sign?",
     "choices": ["The fee request", "A clear interview process", "A written job description"], "answer": 0,
     "why": "Upfront payment demands are a common job-scam warning sign."},
    {"q": "You suspect a payment scam in India. Which official cybercrime channel can you use?",
     "choices": ["A random social media account", "cybercrime.gov.in or helpline 1930", "A link sent by the caller"], "answer": 1,
     "why": "Use official Indian cybercrime reporting channels and act promptly."},
]

def quiz(request):
    result = None
    if request.method == "POST":
        score = 0
        answers = []
        for i, item in enumerate(QUIZ):
            selected = request.POST.get(f"q{i}", "")
            correct = selected.isdigit() and int(selected) == item["answer"]
            score += int(correct)
            answers.append({"question": item["q"], "correct": correct, "why": item["why"]})
        result = {"score": score, "total": len(QUIZ), "answers": answers}
    return render(request, "core/quiz.html", {"questions": enumerate(QUIZ), "result": result})


@login_required
def saved_guides(request):
    saved = SavedArticle.objects.filter(user=request.user).select_related("article")
    return render(request, "core/saved_guides.html", {"saved": saved})

@login_required
def toggle_saved_article(request, pk):
    from django.views.decorators.http import require_POST
    if request.method != "POST":
        return redirect("awareness")
    article = get_object_or_404(AwarenessArticle, pk=pk)
    saved, created = SavedArticle.objects.get_or_create(user=request.user, article=article)
    if not created:
        saved.delete()
        messages.info(request, "Guide removed from your saved list.")
    else:
        messages.success(request, "Guide saved to your personal library.")
    return redirect(request.POST.get("next") or "awareness")

@login_required
def safety_checklist(request):
    checklist, _ = SafetyChecklist.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = SafetyChecklistForm(request.POST, instance=checklist)
        if form.is_valid():
            form.save()
            messages.success(request, "Your safety checklist has been updated.")
            return redirect("safety_checklist")
    else:
        form = SafetyChecklistForm(instance=checklist)
    return render(request, "core/safety_checklist.html", {"form": form, "checklist": checklist})

def trends(request):
    from django.db.models import Count
    from django.db.models.functions import TruncDate
    category_counts = list(IncidentReport.objects.values("category").annotate(total=Count("id")).order_by("-total"))
    status_counts = list(IncidentReport.objects.values("status").annotate(total=Count("id")).order_by("status"))
    total = IncidentReport.objects.count()
    return render(request, "core/trends.html", {
        "category_counts": category_counts,
        "status_counts": status_counts,
        "total": total,
    })
