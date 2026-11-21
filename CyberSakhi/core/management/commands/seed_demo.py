from django.core.management.base import BaseCommand
from core.models import AwarenessArticle

ARTICLES = [
    {
        "title": "Recognising phishing messages", "category": "Phishing",
        "summary": "Spot messages that imitate banks, delivery services or familiar brands.",
        "content": "Phishing messages try to persuade you to reveal information or visit a deceptive website. They may imitate a trusted organisation and create urgency.",
        "warning_signs": "Unexpected account warnings\nUrgent threats or prize claims\nUnexpected attachments or links\nSender address that does not match the organisation",
        "prevention": "Do not open unexpected links or attachments\nVisit the official website by typing its address yourself\nNever share passwords, PINs or OTPs\nReport suspicious messages through official channels"
    },
    {
        "title": "UPI and payment safety", "category": "Payments",
        "summary": "Understand collect requests, QR-code tricks and payment PIN safety.",
        "content": "A UPI PIN is used to authorise payments. Be alert to requests that ask you to enter a PIN to receive money or claim a refund.",
        "warning_signs": "Being asked to enter a PIN to receive money\nUnknown collect requests\nPressure to scan a QR code for a refund\nRequests to install remote-access apps",
        "prevention": "Read the payment screen before approving\nNever disclose your UPI PIN or OTP\nDecline unknown collect requests\nContact your bank through its official app or verified number"
    },
    {
        "title": "Avoiding fake job and task offers", "category": "Employment",
        "summary": "Check work-from-home offers that promise unusually high returns.",
        "content": "Fraudulent job offers may request registration fees, deposits or repeated payments before allowing withdrawals.",
        "warning_signs": "Upfront registration or training fees\nGuaranteed high income for simple tasks\nPressure to pay quickly\nNo verifiable company details",
        "prevention": "Verify the company independently\nDo not pay to unlock earnings\nCheck official company career pages\nDiscuss suspicious offers with a trusted person"
    },
    {
        "title": "Social media impersonation", "category": "Social Media",
        "summary": "Protect yourself when someone creates a fake profile or asks for money.",
        "content": "Impersonators may copy profile photos and contact friends or family with urgent requests.",
        "warning_signs": "A new account claiming to be someone you know\nUrgent requests for money or codes\nUnusual links sent by a familiar account",
        "prevention": "Verify through a separate known contact method\nEnable multi-factor authentication\nUse platform reporting tools\nTell friends if an account is impersonating you"
    },
]

class Command(BaseCommand):
    help = "Add sample CyberSakhi awareness articles"

    def handle(self, *args, **options):
        for item in ARTICLES:
            AwarenessArticle.objects.get_or_create(title=item["title"], defaults=item)
        self.stdout.write(self.style.SUCCESS("Sample awareness articles are ready."))
