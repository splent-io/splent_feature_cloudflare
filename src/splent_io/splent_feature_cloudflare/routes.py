from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from splent_io.splent_feature_cloudflare import cloudflare_bp
from splent_framework.services.service_locator import service_proxy


# =====================================================================
# ADMIN — Captcha (Cloudflare Turnstile) settings
# =====================================================================
@cloudflare_bp.route("/admin/captcha", methods=["GET", "POST"])
@login_required
def admin_settings():
    """Edit the Turnstile keys from the admin (runtime, no .env edit needed)."""
    if request.method == "POST":
        site_key = (request.form.get("site_key") or "").strip()
        secret_key = (request.form.get("secret_key") or "").strip()
        service_proxy("SettingsService").set_many(
            {
                "turnstile_site_key": site_key,
                "turnstile_secret_key": secret_key,
            }
        )
        flash("Captcha settings saved.", "success")
        return redirect(url_for("cloudflare.admin_settings"))
    return render_template("cloudflare/admin/settings.html")
