from rest_framework.response import Response
from rest_framework import status
from enum import StrEnum


class ResponseStatus(StrEnum):
    SUCCESS = "Success"
    FAILURE = "Failure"
    IN_PROGRESS = "In Progress"
    NOT_FOUND = "Not Found"
    CONFLICT = "Conflict"
    UNAUTHORIZED = "Unauthorized"
    FORBIDDEN = "Forbidden"
    INVALID_INPUT = "Invalid Input"
    TIMEOUT = "Timeout"
    UNAVAILABLE = "Service Unavailable"

    def __repr__(self):
        return f"{self.value}"

    def __str__(self):
        return f"{self.value}"


def SuccessResponse(data):
    return Response(
        {"status": ResponseStatus.SUCCESS, "data": data},
        status=status.HTTP_200_OK,
    )


def FailureResponse(data):
    return Response(
        {"status": ResponseStatus.FAILURE, "data": data},
        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,
    )


def CreatedResponse(data):
    return Response(
        {"status": ResponseStatus.SUCCESS, "data": data}, status=status.HTTP_201_CREATED
    )


def BadRequestResponse(data):
    return Response(
        {"status": ResponseStatus.FAILURE, "data": data},
        status=status.HTTP_400_BAD_REQUEST,
    )


def UnauthorizedResponse(data):
    return Response(
        {"status": ResponseStatus.FAILURE, "data": data},
        status=status.HTTP_401_UNAUTHORIZED,
    )


def ForbiddenResponse(data):
    return Response(
        {"status": ResponseStatus.FAILURE, "data": data},
        status=status.HTTP_403_FORBIDDEN,
    )


def NotFoundResponse(data):
    return Response(
        {"status": ResponseStatus.FAILURE, "data": data},
        status=status.HTTP_404_NOT_FOUND,
    )


def ConflictResponse(data):
    return Response(
        {"status": ResponseStatus.FAILURE, "data": data},
        status=status.HTTP_409_CONFLICT,
    )


def ServerErrorResponse(data):
    return Response(
        {"status": ResponseStatus.FAILURE, "data": data},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def InProgressResponse(data):
    return Response(
        {"status": ResponseStatus.IN_PROGRESS, "data": data},
        status=status.HTTP_102_PROCESSING,
    )


def NotFoundResponse(data):
    return Response(
        {"status": ResponseStatus.NOT_FOUND, "data": data},
        status=status.HTTP_404_NOT_FOUND,
    )


def UnauthorizedResponse(data):
    return Response(
        {"status": ResponseStatus.UNAUTHORIZED, "data": data},
        status=status.HTTP_401_UNAUTHORIZED,
    )


def ForbiddenResponse(data):
    return Response(
        {"status": ResponseStatus.FORBIDDEN, "data": data},
        status=status.HTTP_403_FORBIDDEN,
    )


def InvalidInputResponse(data):
    return Response(
        {"status": ResponseStatus.INVALID_INPUT, "data": data},
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def TimeoutResponse(data):
    return Response(
        {"status": ResponseStatus.TIMEOUT, "data": data},
        status=status.HTTP_504_GATEWAY_TIMEOUT,
    )


def ServiceUnavailableResponse(data):
    return Response(
        {"status": ResponseStatus.UNAVAILABLE, "data": data},
        status=status.HTTP_503_SERVICE_UNAVAILABLE,
    )
