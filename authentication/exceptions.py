from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    # Appelle le gestionnaire d'exceptions par défaut de DRF
    response = exception_handler(exc, context)

    # Si DRF n'a pas géré l'erreur (par exemple, une erreur 500), on la gère manuellement
    if response is None:
        return Response(
            {
                "error": "Internal server error",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Personnalise la réponse pour inclure uniquement "error" et "status"
    custom_response_data = {
        "error": str(exc),
        "status": response.status_code
    }
    response.data = custom_response_data
    return response