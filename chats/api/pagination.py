from rest_framework.pagination import (
	LimitOffsetPagination,
	PageNumberPagination
	)


# Tweak on a Viewset basis
class CustomPageNumberPagination(PageNumberPagination):
	page_size = 15

	