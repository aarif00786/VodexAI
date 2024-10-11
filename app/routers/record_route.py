from fastapi import HTTPException,APIRouter, Query
from bson import ObjectId
from app.models.models import Record 
from app.config.collections import record_collection
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi import status
from typing import Optional
router = APIRouter()

# CRUD for records
@router.post("/create/", response_model=dict)
async def create_record(record: Record):
    try:
        record_dict = record.dict()
        record_dict['inserted_date'] = datetime.utcnow()
        result = record_collection.insert_one(record_dict)

        if record_dict.get('inserted_date'):
            record_dict['inserted_date'] = record_dict['inserted_date'].isoformat()
        record_dict['_id'] = str(result.inserted_id)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=record_dict)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": str(e)})


@router.get("/records/{id}", response_model=dict)
async def get_record(id: str):
    try:
        record = record_collection.find_one({"_id": ObjectId(id)})
        if record:
            record['_id'] = str(record['_id'])  # Convert ObjectId to string
            if record.get('inserted_date'):
                record['inserted_date'] = record['inserted_date'].isoformat()
            return JSONResponse(status_code=status.HTTP_200_OK, content=record)
        else:
            raise HTTPException(status_code=404, detail="record not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter")
async def filter_records(
    email: Optional[str] = Query(None, description="Filter by email"),
    location:  Optional[str] = Query(None, description="records by location")
):
    
    try:
        pipeline = []
    
        # Add email filter if provided
        if email:
            pipeline.append({"$match": {"email": email}})
        
        if location:
            pipeline.append({"$match": {"location": location}})
      
        # Execute the aggregation query
        records = list(record_collection.aggregate(pipeline))
        
        # Convert ObjectId to string for the response
        for record in records:
            record["_id"] = str(record["_id"])
        
        if records:
            return records
        
        else:
            raise HTTPException(status_code=404, detail="record not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{id}", response_model=dict)
async def delete_record(id: str):
    try:
        result = record_collection.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 1:
            return {"message": "record deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="record not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/update/{id}", response_model=dict)
async def update_record(id: str, record: Record):
    try:
        # Remove inserted_date from updates (it should not be updated)
        update_data = record.dict(exclude_unset=True)
        update_data.pop('inserted_date', None)

        result = record_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        if result.matched_count == 1:
            return {"message": "record updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="record not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))