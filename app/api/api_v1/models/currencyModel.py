from pydantic import BaseModel, Field


class CurrencyInput(BaseModel):
    id: str = Field(title="Currency ID", description="Currency id, e.g. bitcoin")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "bitcoin",
                }
            ]
        }
    }


class CurrencyOutput(BaseModel):
    id: str = Field(title="Currency ID", description="Unique currency id")
    symbol: str = Field(title="Currency Symbol", description="Unique currency symbol")
    name: str = Field(title="Currency Name", description="Currency name")
    meta: str = Field(title="Currency Meta", description="Currency meta information")


class CurrencyItem(BaseModel):
    id: str
    symbol: str
    name: str
    meta: str
