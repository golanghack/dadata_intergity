import itertools

from drf_spectacular.drainage import error, warn
from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.generators import EndpointEnumerator, SchemaGenerator
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import build_media_type_object, get_class
from drf_spectacular.utils import OpenApiRequest
from rest_framework import views, viewsets
from rest_framework.request import clone_request
from rest_framework.settings import api_settings


class CustomEndpointEnumerator(EndpointEnumerator):
    def get_allowed_methods(self, callback):
        """Перегружает метод из базового класса
        в базовом классе OPTIONS удален из разрешенных методов."""
        non_allowed_methods = ("OPTIONS", "HEAD", "TRACE", "CONNECT")
        if hasattr(callback, "actions"):
            actions = set(callback.actions)
            if "options" in actions:
                non_allowed_methods = ("HEAD", "TRACE", "CONNECT")
            if "http_method_names" in callback.initkwargs:
                http_method_names = set(
                    callback.initkwargs["http_method_names"]
                )
            else:
                http_method_names = set(callback.cls.http_method_names)

            methods = [
                method.upper() for method in actions & http_method_names
            ]
        else:
            
            kwargs = {}
            if "http_method_names" in callback.initkwargs:
                kwargs["http_method_names"] = callback.initkwargs[
                    "http_method_names"
                ]

            methods = callback.cls(**kwargs).allowed_methods

        return [
            method for method in methods if method not in non_allowed_methods
        ]


class CustomSchemaGenerator(SchemaGenerator):
    endpoint_inspector_cls = CustomEndpointEnumerator

    def base_create_view(self, callback, method, request=None):
        """
        Given a callback, return an actual view instance.
        """
        view = callback.cls(**getattr(callback, "initkwargs", {}))
        view.args = ()
        view.kwargs = {}
        view.format_kwarg = None
        view.request = None
        view.action_map = getattr(callback, "actions", None)

        actions = getattr(callback, "actions", None)
        if actions is not None:
            view.action = actions.get(method.lower())

        if request is not None:
            view.request = clone_request(request, method)

        return view

    def create_view(
        self,
        callback,
        method,
        request=None,  # noqa: ARG002
    ):

        override_view = OpenApiViewExtension.get_match(callback.cls)
        if override_view:
            original_cls = callback.cls
            callback.cls = override_view.view_replacement()
        view = self.base_create_view(callback, method, None)
        view.swagger_fake_view = True
        if override_view:
            callback.cls = original_cls

        if isinstance(view, viewsets.ViewSetMixin):
            action = getattr(view, view.action)
        elif isinstance(view, views.APIView) and method.lower() != "options":
            action = getattr(view, method.lower())
        else:
            error(
                "Using not supported View class. "
                "Class must be derived from APIView "
                "or any of its subclasses like GenericApiView, GenericViewSet."
            )
            return view

        action_schema = getattr(action, "kwargs", {}).get("schema", None)
        if not action_schema:
            return view

        action_schema_class = get_class(action_schema)
        view_schema_class = get_class(callback.cls.schema)

        if not issubclass(action_schema_class, view_schema_class):
            mro = (
                tuple(
                    cls
                    for cls in action_schema_class.__mro__
                    if cls not in api_settings.DEFAULT_SCHEMA_CLASS.__mro__
                )
                + view_schema_class.__mro__
            )
            action_schema_class = type("ExtendedRearrangedSchema", mro, {})

        view.schema = action_schema_class()
        return view


class CustomAutoSchema(AutoSchema):
    method_mapping = {
        "get": "retrieve",
        "post": "create",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
        "options": "options",
    }

    def _get_request_body(self, direction="request"):
        if self.method not in ("OPTIONS", "PUT", "PATCH", "POST"):
            return None

        request_serializer = self.get_request_serializer()
        request_body_required = True
        content = []
        if isinstance(request_serializer, dict):
            media_types_iter = request_serializer.items()
        else:
            media_types_iter = zip(
                self.map_parsers(), itertools.repeat(request_serializer)
            )

        for media_type, serializer in media_types_iter:
            if isinstance(serializer, OpenApiRequest):
                serializer, examples, encoding = (
                    serializer.request,
                    serializer.examples,
                    serializer.encoding,
                )
            else:
                encoding, examples = None, None

            if (
                encoding
                and media_type != "application/x-www-form-urlencoded"
                and not media_type.startswith("multipart")
            ):
                warn(
                    'Encodings object on media types other than '
                    '"application/x-www-form-urlencoded" '
                    'or "multipart/*" have undefined behavior.'
                )

            examples = self._get_examples(
                serializer, direction, media_type, None, examples
            )
            schema, partial_request_body_required = (
                self._get_request_for_media_type(serializer, direction)
            )

            if schema is not None:
                content.append((media_type, schema, examples, encoding))
                request_body_required &= partial_request_body_required

        if not content:
            return None

        request_body = {
            "content": {
                media_type: build_media_type_object(schema, examples, encoding)
                for media_type, schema, examples, encoding in content
            }
        }
        if request_body_required:
            request_body["required"] = request_body_required
        return request_body
