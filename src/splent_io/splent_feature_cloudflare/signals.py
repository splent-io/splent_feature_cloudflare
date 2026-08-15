"""Anti-spam: validate submitted comments with Cloudflare Turnstile.

Listens to the comments feature's ``comment-submitting`` signal. There is NO
hard dependency on comments — if comments isn't installed the signal is never
defined and this handler is simply skipped.
"""

from splent_framework.signals.signal_utils import connect_signal


@connect_signal("comment-submitting", "splent_feature_cloudflare")
def validate_turnstile(sender, form=None, remoteip=None, **kwargs):
    from splent_io.splent_feature_cloudflare.services import CloudflareService

    token = form.get("cf-turnstile-response") if form else None
    return CloudflareService().verify(token, remoteip)


@connect_signal("contact-submitting", "splent_feature_cloudflare")
def validate_turnstile_contact(sender, form=None, remoteip=None, **kwargs):
    from splent_io.splent_feature_cloudflare.services import CloudflareService

    token = form.get("cf-turnstile-response") if form else None
    return CloudflareService().verify(token, remoteip)


@connect_signal("careers-submitting", "splent_feature_cloudflare")
def validate_turnstile_careers(sender, form=None, remoteip=None, **kwargs):
    from splent_io.splent_feature_cloudflare.services import CloudflareService

    token = form.get("cf-turnstile-response") if form else None
    return CloudflareService().verify(token, remoteip)
