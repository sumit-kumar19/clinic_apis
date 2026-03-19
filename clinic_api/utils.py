from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def success_response(data=None, message="Success", http_status=200):
    return Response(
        {
            "success": True,
            "data": data,
            "message": message,
        },
        status=http_status
    )


def error_response(message="Error", data=None, http_status=400):
    return Response(
        {
            "success": False,
            "data": data,
            "message": message,
        },
        status=http_status
    )


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        original_data = response.data
        if isinstance(original_data, dict):
            message = str(list(original_data.values())[0]) if original_data else "Error occured"
        elif isinstance(original_data, list):
            message = str(original_data[0]) if original_data else "Error occured"
        else:
            message = str(original_data)

        response.data = {
            "success": False,
            "data": original_data,
            "message": message,
        }

    return response


def handle_404(request, exception):
    return error_response(message="not found.", http_status=404)


def handle_500(request):
    return error_response(message="server error.", http_status=500)
