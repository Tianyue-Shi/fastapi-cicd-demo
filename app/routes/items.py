from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException

from app.database import get_database
from app.models import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(prefix="/api/items", tags=["items"])


def _to_response(doc: dict) -> ItemResponse:
    """Convert a MongoDB document to an ItemResponse."""
    return ItemResponse(
        id=str(doc["_id"]),
        name=doc["name"],
        description=doc["description"],
        price=doc["price"],
        quantity=doc["quantity"],
    )


def _validate_object_id(item_id: str) -> ObjectId:
    """Validate and convert a string to a BSON ObjectId."""
    try:
        return ObjectId(item_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail=f"Invalid item ID: {item_id}")


def _require_db():
    """Get the database or raise 503 if unavailable."""
    db = get_database()
    if db is None:
        raise HTTPException(
            status_code=503,
            detail="Database is not available. Please try again later.",
        )
    return db


@router.get("/", response_model=list[ItemResponse])
async def list_items():
    """List all items."""
    db = _require_db()
    items = []
    cursor = db.items.find()
    async for document in cursor:
        items.append(_to_response(document))
    return items


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    """Get a single item by its ID."""
    db = _require_db()
    oid = _validate_object_id(item_id)
    document = await db.items.find_one({"_id": oid})
    if document is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return _to_response(document)


@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    """Create a new item."""
    db = _require_db()
    item_dict = item.model_dump()
    result = await db.items.insert_one(item_dict)
    item_dict["_id"] = result.inserted_id
    return _to_response(item_dict)


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: ItemUpdate):
    """Update an existing item. Only provided fields are updated."""
    db = _require_db()
    oid = _validate_object_id(item_id)

    # Build update dict from non-None fields only
    update_data = {k: v for k, v in item.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await db.items.find_one_and_update(
        {"_id": oid},
        {"$set": update_data},
        return_document=True,
    )
    if result is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return _to_response(result)


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: str):
    """Delete an item by its ID."""
    db = _require_db()
    oid = _validate_object_id(item_id)
    result = await db.items.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return None