from pydantic import BaseModel, Field
from typing import List
from enum import Enum


class MethodTypes(str, Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class InputModel(BaseModel):
    urls: List[str] = Field(
        description="List of URLs to make requests to."
    )
    method: MethodTypes = Field(
        default=MethodTypes.GET,
        description="HTTP method to use for all requests."
    )
    bearer_token: str = Field(
        default=None,
        description="Bearer token to use for authentication."
    )
    body_json_data: str = Field(
        default="""{
    "key_1": "value_1",
    "key_2": "value_2"
}
""",
        description="JSON data to send in the request body (applied to all requests).",
        json_schema_extra={
            'widget': "codeeditor-json",
        }
    )


class OutputModel(BaseModel):
    base64_bytes_data_list: List[str] = Field(
        description='Output data for each URL as a list of base64 encoded strings.'
    )
