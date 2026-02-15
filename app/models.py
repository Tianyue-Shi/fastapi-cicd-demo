from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    """Schema for creating a new item (request body)."""
    name: str = Field(..., min_length=1, max_length=100, examples=["Widget"])
    description: str = Field(
        ..., min_length=1, max_length=500, examples=["A useful widget"]
    )
    price: float = Field(..., gt=0, examples=[9.99])
    quantity: int = Field(..., ge=0, examples=[100])


class ItemUpdate(BaseModel):
    """Schema for updating an existing item (request body)."""
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, min_length=1, max_length=500)
    price: float | None = Field(None, gt=0)
    quantity: int | None = Field(None, ge=0)


class ItemResponse(BaseModel):
    """Schema for an item returned in API responses."""
    id: str
    name: str
    description: str
    price: float
    quantity: int