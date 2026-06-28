from splent_framework.blueprints.base_blueprint import create_blueprint
from splent_framework.services.service_locator import register_service, service_proxy

from splent_io.splent_feature_cloudflare.services import CloudflareService

cloudflare_bp = create_blueprint(__name__)


def init_feature(app):
    # Registered under the GENERIC "CaptchaService" name so consumers (e.g.
    # comments) stay provider-agnostic. This is the Cloudflare Turnstile
    # implementation of the 'captcha' alternative (recaptcha is the other).
    register_service(app, "CaptchaService", CloudflareService)


def inject_context_vars(app):
    # Generic captcha helpers so templates work with any provider:
    #   {{ captcha_script() }}  (once on the page)
    #   {{ captcha_widget() }}  (inside the form)
    def captcha_widget():
        return service_proxy("CaptchaService").widget()

    def captcha_script():
        return service_proxy("CaptchaService").script_tag()

    return {"captcha_widget": captcha_widget, "captcha_script": captcha_script}
