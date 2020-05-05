from rest_framework.response import Response
from rest_framework.serializers import Serializer


class JsonResponse(Response):

    def __init__(self, data=None, code=2000, message='success', detail=None, status=None,
                 template_name=None, headers=None, exception=False, content_type=None):

        super(Response, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = {"code": code, "message": message, "data": data}
        if detail:
            self.data['detail'] = detail
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value
