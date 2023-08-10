import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration


def add_sentry(dsn: str, environment: str) -> None:
    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        debug=False,
        sample_rate=1.0,
        max_breadcrumbs=100,
        attach_stacktrace=False,
        send_default_pii=False,
        with_locals=True,
        traces_sample_rate=0.0,
        default_integrations=True,
        integrations=[StarletteIntegration(), FastApiIntegration()],
    )
