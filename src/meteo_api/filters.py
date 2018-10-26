import coreapi
import coreschema
from rest_framework.filters import BaseFilterBackend


class ForecastsListFilterBackend(BaseFilterBackend):

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='type',
                required=False,
                schema=coreschema.String(
                    description="Temperature type.",
                )
            ),
            coreapi.Field(
                name='days',
                required=False,
                schema=coreschema.String(
                    description="Days period.",
                )
            ),
        ]


class ForecastDateListFilterBackend(BaseFilterBackend):

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name='type',
                required=False,
                schema=coreschema.String(
                    description="Temperature type.",
                )
            ),
            coreapi.Field(
                name='hour',
                required=False,
                schema=coreschema.String(
                    description="Current hour.",
                )
            ),
        ]