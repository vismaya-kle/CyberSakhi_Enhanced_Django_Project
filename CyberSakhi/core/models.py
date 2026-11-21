import uuid
from django.conf import settings
from django.db import models

class IncidentReport(models.Model):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("reviewing", "Under review"),
        ("action", "Action recommended"),
        ("closed", "Closed"),
    ]
    CATEGORY_CHOICES = [
        ("upi", "UPI / Payment scam"),
        ("phishing", "Phishing link or email"),
        ("social", "Social media impersonation"),
        ("job", "Job / task scam"),
        ("shopping", "Shopping / delivery scam"),
        ("other", "Other"),
    ]
    reference_id = models.CharField(max_length=12, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="incident_reports")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=120)
    description = models.TextField()
    incident_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="submitted")
    admin_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference_id:
            self.reference_id = "CS-" + uuid.uuid4().hex[:7].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_id} — {self.title}"

class AwarenessArticle(models.Model):
    title = models.CharField(max_length=140)
    category = models.CharField(max_length=60)
    summary = models.CharField(max_length=240)
    content = models.TextField()
    warning_signs = models.TextField(help_text="One warning sign per line")
    prevention = models.TextField(help_text="One prevention tip per line")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category", "title"]

    def __str__(self):
        return self.title

class SavedArticle(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_guides")
    article = models.ForeignKey(AwarenessArticle, on_delete=models.CASCADE, related_name="saved_by")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "article"], name="unique_saved_article_per_user")]
        ordering = ["-saved_at"]

    def __str__(self):
        return f"{self.user} saved {self.article}"


class SafetyChecklist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="safety_checklist")
    mfa_enabled = models.BooleanField(default=False)
    unique_passwords = models.BooleanField(default=False)
    device_lock = models.BooleanField(default=False)
    software_updated = models.BooleanField(default=False)
    backups_enabled = models.BooleanField(default=False)
    recovery_options = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def score(self):
        fields = [self.mfa_enabled, self.unique_passwords, self.device_lock,
                  self.software_updated, self.backups_enabled, self.recovery_options]
        return round(sum(fields) / len(fields) * 100)

    def __str__(self):
        return f"{self.user}'s safety checklist ({self.score}%)"
