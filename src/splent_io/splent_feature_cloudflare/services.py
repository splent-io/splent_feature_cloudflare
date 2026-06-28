import requests
from flask import current_app
from markupsafe import Markup

VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


class CloudflareService:
    """Cloudflare Turnstile — a CAPTCHA that protects forms from spam.

    A utility service with no DB model. Registered under the generic
    ``CaptchaService`` name so consumers stay provider-agnostic. Templates use
    the captcha_widget()/captcha_script() helpers; routes call
    ``verify(token, remoteip)`` before accepting a submission.
    """

    def site_key(self):
        return current_app.config.get("TURNSTILE_SITE_KEY", "")

    def enabled(self):
        return bool(self.site_key())

    def widget(self):
        """The Turnstile widget markup to drop inside a form."""
        key = self.site_key()
        if not key:
            return Markup("")
        return Markup(f'<div class="cf-turnstile" data-sitekey="{key}"></div>')

    def script_tag(self):
        """The Turnstile JS, to include once on a page that renders the widget."""
        if not self.enabled():
            return Markup("")
        return Markup(
            '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js"'
            " async defer></script>"
        )

    def verify(self, token, remoteip=None):
        """Validate a Turnstile token with Cloudflare. Returns True/False.

        If no secret is configured, returns True (does not block submissions).
        """
        secret = current_app.config.get("TURNSTILE_SECRET_KEY", "")
        if not secret:
            return True
        if not token:
            return False
        try:
            data = {"secret": secret, "response": token}
            if remoteip:
                data["remoteip"] = remoteip
            resp = requests.post(VERIFY_URL, data=data, timeout=10)
            return bool(resp.json().get("success"))
        except Exception:
            return False
