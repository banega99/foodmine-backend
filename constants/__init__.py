from enum import Enum

HTTP_BAD_REQUEST = 400


class OrderStatus(Enum):
    NEW = 'NEW'
    PAYED = 'PAYED'
    SHIPPED = 'SHIPPED'
    CANCELED = 'CANCELED'
    REFUNDED = 'REFUNDED'
