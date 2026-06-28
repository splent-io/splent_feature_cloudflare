import requests
from flask import current_app
from markupsafe import Markup

from splent_framework.services.service_locator import service_proxy

VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


class CloudflareService:
    """Cloudflare Turnstile — a CAPTCHA that protects forms from spam.

    A utility service with no DB model. Registered under the generic
    ``CaptchaService`` name so consumers stay provider-agnostic. Templates use
    the captcha_widget()/captcha_script() helpers; routes call
    ``verify(token, remoteip)`` before accepting a submission.

    Keys are read from the admin-editable SettingsService first (so they can be
    changed at runtime from the admin panel), falling back to the product's
    config/.env (TURNSTILE_SITE_KEY / TURNSTILE_SECRET_KEY).
    """

    def _setting(self, key):
        """Read an admin-editable setting, tolerating an absent SettingsService."""
        try:
            return service_proxy("SettingsService").get(key, None)
        except Exception:
            return None

    def site_key(self):
        return self._setting("turnstile_site_key") or current_app.config.get(
            "TURNSTILE_SITE_KEY", ""
        )

    def secret_key(self):
        return self._setting("turnstile_secret_key") or current_app.config.get(
            "TURNSTILE_SECRET_KEY", ""
        )

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
        secret = self.secret_key()
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
