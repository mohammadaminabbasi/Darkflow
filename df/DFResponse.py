from django.http import JsonResponse


def DFResponse(is_successful=True, data=None, message=""):
    response = {
        "isSuccessful": is_successful,
        "message": str(message),
        "data": data
    }
    return JsonResponse(data=response, safe=False)
