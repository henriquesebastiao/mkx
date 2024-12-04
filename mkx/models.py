from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress


class IPAddress(BaseModel):
    ip: IPvAnyAddress
