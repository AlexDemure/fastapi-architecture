import json
import logging
from contextlib import contextmanager
from enum import IntEnum
from functools import wraps
from typing import Callable
from typing import Optional

from opentelemetry import trace
from opentelemetry.context import Context
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace import _Span as Span
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Tracer
from opentelemetry.trace.propagation import set_span_in_context
from opentelemetry.trace.span import NonRecordingSpan
from opentelemetry.trace.span import SpanContext
from opentelemetry.trace.span import TraceFlags

from app.core.serializer import DatetimeAwareJSONEncoder
from app.core.settings import config
from app.exceptions.business import BusinessError
from app.exceptions.crud import CRUDError


def add_jaeger(service_name: str, endpoint: str) -> None:
    jaeger_exporter = OTLPSpanExporter(
        endpoint=f"{endpoint}/api/traces?format=jaeger.thrift",
        insecure=True,
    )
    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace_provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    trace_provider.add_span_processor(span_processor)
    trace.set_tracer_provider(trace_provider)


def get_tracer(name: str = __name__) -> Tracer:
    """name - otel.library.name."""
    return trace.get_tracer(name)


tracer = get_tracer(config.PROJECT_NAME)


class TracingLevel(IntEnum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG


class Tracing:
    span: Span = None

    def __init__(self, span: Span) -> None:
        self.span = span

    def write_log(self, message: str, **kwargs) -> None:
        attributes = dict()

        # When running tests, the span type is changed to NonRecordingSpan which has no attributes
        if getattr(self.span, "attributes", None):
            for key, value in self.span.attributes.items():
                if not kwargs.get(key, None):
                    kwargs[key] = value

        for kwarg in kwargs:
            if isinstance(kwargs[kwarg], (dict, list)):
                attributes[kwarg] = json.dumps(kwargs[kwarg], cls=DatetimeAwareJSONEncoder, ensure_ascii=False)
            else:
                attributes[kwarg] = str(kwargs[kwarg])

        self.span.add_event(message, attributes=attributes)

    def set_tags(self, **kwargs) -> None:
        for kwarg in kwargs:
            self.span.set_attribute(kwarg, kwargs[kwarg] if kwargs[kwarg] else "")

    def debug(self, message: str, **kwargs) -> None:
        self.write_log(message, **kwargs)

    def error(self, message: str, **kwargs) -> None:
        self.write_log(message, **kwargs)

    def info(self, message: str, **kwargs) -> None:
        self.write_log(message, **kwargs)

    def warning(self, message: str, **kwargs) -> None:
        self.write_log(message, **kwargs)

    def object_created(self, object_name: str, created_fields: dict, **kwargs) -> None:
        self.debug(f"{object_name} is created", created_fields=created_fields, **kwargs)

    @classmethod
    def get_context(cls, trace_id: Optional[str] = None, span_id: Optional[str] = None) -> Optional[Context]:
        if trace_id:
            parent_span_context = SpanContext(
                trace_id=int(trace_id, 16),
                # Добавление трейса на корневой уровень если span_id не передан
                span_id=int(span_id, 16) if span_id else 1,
                is_remote=True,
                trace_flags=TraceFlags(1),
            )
            parent_span = NonRecordingSpan(parent_span_context)
            context_for_new_span = set_span_in_context(parent_span)
            return context_for_new_span

    @property
    def trace_id(self):
        return trace.format_trace_id(self.span.context.trace_id)

    @property
    def span_id(self):
        return trace.format_span_id(self.span.context.span_id)


def _get_name(function_: Callable) -> str:
    return f"{function_.__module__}.{function_.__name__}"  # type:ignore


@contextmanager
def _new_span(
    name: str,
    trace_id: Optional[str] = None,
    span_id: Optional[str] = None,
) -> Span:
    with tracer.start_as_current_span(name, context=Tracing.get_context(trace_id, span_id)) as span:
        yield span


@contextmanager
def _new_non_recording_span() -> NonRecordingSpan:
    context = SpanContext(trace_id=1, span_id=1, is_remote=True, trace_flags=TraceFlags(0))
    with NonRecordingSpan(context) as span:
        yield span


def decorator_tracing(return_tracing: bool, level: TracingLevel = TracingLevel.DEBUG):
    def decorator(function_):
        @wraps(function_)
        async def wrapper(*args, **kwargs):
            name = _get_name(function_=function_)

            error = None

            if level >= getattr(TracingLevel, config.TRACING_LEVEL.upper()):
                context = _new_span(name)
            else:
                context = _new_non_recording_span()

            with context as span:
                tracing = Tracing(span)

                try:
                    if return_tracing:
                        value = await function_(tracing=tracing, *args, **kwargs)
                    else:
                        value = await function_(*args, **kwargs)
                except (CRUDError, BusinessError) as e:
                    span.record_exception(e)
                    error = e

            if error:
                raise error

            return value

        return wrapper

    return decorator


@contextmanager
def context_tracing(
    function_: Callable,
    trace_id: Optional[str] = None,
    span_id: Optional[str] = None,
    level: TracingLevel = TracingLevel.DEBUG,
) -> Tracing:
    name = _get_name(function_=function_)

    error = None

    if level >= getattr(TracingLevel, config.TRACING_LEVEL.upper()):
        context = _new_span(name, trace_id, span_id)
    else:
        context = _new_non_recording_span()

    with context as span:
        tracing = Tracing(span)

        try:
            yield tracing
        except (CRUDError, BusinessError) as e:
            span.record_exception(e)
            error = e

    if error:
        raise error
