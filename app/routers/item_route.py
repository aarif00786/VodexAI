from fastapi import HTTPException,APIRouter, Query
from bson import ObjectId
from app.models.models import Item 
from app.config.collections import item_collection
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi import status
from typing import Optional
router = APIRouter()
# API to print "Hello World"
@router.get("/get-hello/")
async def read_root():
    return {"message": "Hello World"}

# CRUD for Items
@router.post("/create/", response_model=dict)
async def create_item(item: Item):
    try:
        item_dict = item.dict()
        item_dict['inserted_date'] = datetime.utcnow()
        result = item_collection.insert_one(item_dict)

        if item_dict.get('inserted_date'):
            item_dict['inserted_date'] = item_dict['inserted_date'].isoformat()
        if item_dict.get('expiry_date'):
            item_dict['expiry_date'] = item_dict['expiry_date'].isoformat()

        item_dict['_id'] = str(result.inserted_id)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=item_dict)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(e)})


@router.get("/items/{id}", response_model=dict)
async def get_item(id: str):
    try:
        item = item_collection.find_one({"_id": ObjectId(id)})
        if item:
            item['_id'] = str(item['_id'])  # Convert ObjectId to string
            if item.get('inserted_date'):
                item['inserted_date'] = item['inserted_date'].isoformat()
            if item.get('expiry_date'):
                item['expiry_date'] = item['expiry_date'].isoformat()
            return JSONResponse(status_code=status.HTTP_200_OK, content=item)
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter")
async def filter_items(
    email: Optional[str] = Query(None, description="Filter by email"),
    expiry_date: Optional[datetime] = Query(None, description="Items expiring after this date"),
    inserted_date: Optional[datetime] = Query(None, description="Items inserted after this date"),
    quantity: Optional[int] = Query(None, description="Items with quantity greater than or equal to this number")
):
    
    try:
        pipeline = []
    
        # Add email filter if provided
        if email:
            pipeline.append({"$match": {"email": email}})
        
        # Add expiry_date filter if provided
        if expiry_date:
            pipeline.append({
                "$match": {
                    "expiry_date": {"$gt": expiry_date}
                }
            })
        
        # Add inserted_date filter if provided
        if inserted_date:
            pipeline.append({
                "$match": {
                    "inserted_date": {"$gt": inserted_date}
                }
            })
        
        # Add quantity filter if provided
        if quantity:
            pipeline.append({
                "$match": {
                    "quantity": {"$gte": quantity}
                }
            })

        # Execute the aggregation query
        items = list(item_collection.aggregate(pipeline))
        
        # Convert ObjectId to string for the response
        for item in items:
            item["_id"] = str(item["_id"])
        
        if items:
            return items
        
        else:
            raise HTTPException(status_code=404, detail="Item not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{id}", response_model=dict)
async def delete_item(id: str):
    try:
        result = item_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return {"message": "Item deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/update/{id}", response_model=dict)
async def update_item(id: str, item: Item):
    try:
        # Remove inserted_date from updates (it should not be updated)
        update_data = item.dict(exclude_unset=True)
        update_data.pop('inserted_date', None)

        result = item_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        if result.matched_count == 1:
            return {"message": "Item updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))