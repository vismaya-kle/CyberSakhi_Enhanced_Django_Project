import re
from urllib.parse import urlparse

KEYWORDS = [
    "urgent", "verify your account", "account blocked", "suspended",
    "claim prize", "winner", "lottery", "otp", "password", "kyc",
    "refund", "payment failed", "click here", "limited time",
    "remote access", "screen sharing", "processing fee", "job offer",
]
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly", "rb.gy"}

def analyse_text(value):
    text = (value or "").strip()
    lower = text.lower()
    signals = []
    score = 0

    if not text:
        return {"score": 0, "level": "Not analysed", "signals": ["Enter a URL, message or email to check."],
                "advice": "Never share OTPs, passwords or payment PINs."}

    found = [word for word in KEYWORDS if word in lower]
    if found:
        score += min(35, 8 * len(found))
        signals.append("Pressure or sensitive-information wording: " + ", ".join(found[:5]))

    urls = re.findall(r'(?:https?://|www\.)[^\s<>"\']+', text, flags=re.I)
    for raw in urls:
        candidate = raw.rstrip(".,!?;:)")
        parsed = urlparse(candidate if candidate.startswith(("http://", "https://")) else "http://" + candidate)
        host = (parsed.hostname or "").lower()
        if host in SHORTENERS:
            score += 25
            signals.append("A URL-shortening service hides the final destination.")
        if host.startswith("xn--") or ".xn--" in host:
            score += 20
            signals.append("The URL contains an internationalised domain label; inspect it carefully.")
        if parsed.scheme == "http":
            score += 10
            signals.append("The link uses HTTP rather than HTTPS.")
        if re.search(r'\d{1,3}(?:\.\d{1,3}){3}', host):
            score += 20
            signals.append("The link uses an IP address instead of a familiar domain name.")

    if "@" in text and "http" in lower:
        score += 10
        signals.append("The text combines an email-like address and a link; verify the sender independently.")

    score = min(score, 100)
    if score >= 55:
        level = "High"
    elif score >= 25:
        level = "Medium"
    else:
        level = "Low"

    if not signals:
        signals.append("No common warning patterns were detected by this basic checker.")
    advice = ("Do not open the link or share information. Verify through the organisation's official app or website."
              if level == "High" else
              "Pause and verify the sender and website using a trusted, independent channel."
              if level == "Medium" else
              "Still be cautious. A low score does not prove that content is safe.")
    return {"score": score, "level": level, "signals": signals, "advice": advice}
