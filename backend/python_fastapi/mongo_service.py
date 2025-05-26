from pymongo import MongoClient, ASCENDING
from typing import Dict, Any
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

MONGO_URI     = os.getenv("MONGO_URI")
MONGO_DB      = os.getenv("MONGO_DB")
COLL_MCQS     = os.getenv("COLL_MCQS")
COLL_SEGMENTS = os.getenv("COLL_SEGMENTS")
COLL_POLLING  = os.getenv("COLL_POLLING")

client = MongoClient(MONGO_URI)
db     = client[MONGO_DB]

mcqs_col     = db[COLL_MCQS]
segments_col = db[COLL_SEGMENTS]
polling_col  = db[COLL_POLLING]

# Ensure indexes for FK-like structure
mcqs_col.create_index([("mcqs_id", ASCENDING)], unique=True)
segments_col.create_index([("segment_id", ASCENDING)], unique=True)
polling_col.create_index([("polling_id", ASCENDING)], unique=True)


# ------------------- INSERT FUNCTIONS -------------------

def insert_segment(file_id: int, segment_id: int, text: str) -> str:
    return str(segments_col.insert_one({
        "file_id": file_id,
        "segment_id": segment_id,
        "segments_text": text
    }).inserted_id)


def insert_mcqs(file_id: int, segment_id: int, mcqs_id: int, mcqs_text: str) -> str:
    return str(mcqs_col.insert_one({
        "mcqs_id": mcqs_id,
        "file_id": file_id,
        "segment_id": segment_id,
        "mcqs_id": mcqs_id,
        "mcqs": mcqs_text
    }).inserted_id)


def insert_polling(polling_id: int, file_id: int, percentage: float) -> str:
    return str(polling_col.insert_one({
        "polling_id": polling_id,
        "file_id": file_id,
        "percentage": percentage
    }).inserted_id)


# ------------------- GET FUNCTIONS -------------------

def get_mcqs_by_file_id(file_id: int) -> Dict[str, Any]:
    return mcqs_col.find_one({"file_id": file_id}, {"_id": 0})

def get_mcqs_by_segment_id(segment_id: int) -> Dict[str, Any]:
    return mcqs_col.find_one({"segment_id": segment_id}, {"_id": 0})

def get_mcqs(file_id:int,segment_id: int) -> Dict[str, Any]:
    return mcqs_col.find_one({"file_id": file_id, "segment_id": segment_id}, {"_id": 0})

def get_all_mcqs(file_id:int,segment_id: int) -> Dict[str, Any]:
    return mcqs_col.fin


def get_segment(file_id: int, segment_id: int) -> Dict[str, Any]:
    return segments_col.find_one({"file_id": file_id, "segment_id": segment_id}, {"_id": 0})


def get_polling(polling_id: int) -> Dict[str, Any]:
    return polling_col.find_one({"polling_id": polling_id}, {"_id": 0})


# ------------------- UPDATE FUNCTIONS -------------------

def update_polling_percentage(polling_id: int, new_percentage: float) -> int:
    print(f"Updating polling_id {polling_id} with new percentage: {new_percentage}")
    result = polling_col.update_one(
        {"polling_id": polling_id},
        {"$set": {"percentage": new_percentage}}
    )
    return result.modified_count


# ------------------- DELETE FUNCTIONS -------------------

def delete_mcqs(file_id: int, segment_id: int) -> int:
    return mcqs_col.delete_one({"file_id": file_id, "segment_id": segment_id}).deleted_count


def delete_segment(file_id: int, segment_id: int) -> int:
    return segments_col.delete_one({"file_id": file_id, "segment_id": segment_id}).deleted_count


def delete_polling(polling_id: int) -> int:
    return polling_col.delete_one({"polling_id": polling_id}).deleted_count


# ------------------- DEMO BLOCK -------------------

if __name__ == "__main__":
    file_id = 123
    segment_id = 456
    mcqs_id = 789
    polling_id = 999

    sample_text = "Sample segment transcript..."
    sample_mcqs = """1. Question?\nA) Opt1\nB) Opt2\nC) Opt3\nD) Opt4\n\nCorrect: B"""

    # print("Inserting segment:", insert_segment(file_id, segment_id, sample_text))
    # print("Inserting MCQs:", insert_mcqs(file_id, segment_id, mcqs_id, sample_mcqs))
    # print("Inserting polling data:", insert_polling(polling_id, file_id, 72.5))

    print("Fetching MCQs:", get_mcqs(file_id, segment_id))
    print("Fetching MCQs by file_id:", get_mcqs_by_file_id(file_id))

    print("Fetching Segment:", get_segment(file_id, segment_id))
    print("Fetching Polling:", get_polling(polling_id))
    

    print("Updating Polling %:", update_polling_percentage(polling_id, 0))
    
    print(list(mcqs_col.find({}, {"_id": 0})))
    print(list(segments_col.find({}, {"_id": 0})))
    print(list(polling_col.find({}, {"_id": 0})))

    # Cleanup (uncomment to test)
    # delete_mcqs(file_id, segment_id)
    # delete_segment(file_id, segment_id)
    # delete_polling(polling_id)
