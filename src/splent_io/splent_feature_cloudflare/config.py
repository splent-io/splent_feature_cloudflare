"""Cloudflare Turnstile configuration (a privacy-friendly anti-spam CAPTCHA).

Set TURNSTILE_SITE_KEY / TURNSTILE_SECRET_KEY in the product's .env (dev/prod).
Defaults are Cloudflare's official TEST keys (always pass), so development works
out of the box — set real keys in production.
"""

import os

# Cloudflare's documented test keys: always pass, safe for dev.
_TEST_SITE_KEY = "1x00000000000000000000AA"
_TEST_SECRET_KEY = "1x0000000000000000000000000000000AA"


def inject_config(app):
    app.config.update(
        {
            "TURNSTILE_SITE_KEY": os.getenv("TURNSTILE_SITE_KEY", _TEST_SITE_KEY),
            "TURNSTILE_SECRET_KEY": os.getenv("TURNSTILE_SECRET_KEY", _TEST_SECRET_KEY),
        }
    )
