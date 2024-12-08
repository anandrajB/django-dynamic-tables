from rest_framework.exceptions import APIException


class BaseException(APIException):
    status_code = 500
    default_detail = "Internal server error, try again later."
    default_code = "internal_server_error"


class TableDoesntExistException(APIException):
    status_code = 404
    default_detail = "Table does not exist."
    default_code = "table_doesnt_exist"


class ColumnDoesntExistException(APIException):
    status_code = 404
    default_detail = "Column does not exist."
    default_code = "column_doesnt_exist"
