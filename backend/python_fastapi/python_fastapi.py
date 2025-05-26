from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING
from faster_whisper import WhisperModel
from langchain_groq import ChatGroq
from typing import Dict, Any
import textwrap
import os
from datetime import datetime
from langchain_ollama import ChatOllama
from mongo_service import insert_segment,insert_mcqs,insert_polling,update_polling_percentage,get_mcqs,get_segment,get_mcqs_by_file_id,get_mcqs_by_segment_id,get_polling
from fastapi.middleware.cors import CORSMiddleware
from websocket_manager import manager
from fastapi import WebSocket,WebSocketDisconnect
from typing import List
import asyncio
import json

# Load environment variables
load_dotenv()

MONGO_URI     = os.getenv("MONGO_URI")
MONGO_DB      = os.getenv("MONGO_DB")
COLL_MCQS     = os.getenv("COLL_MCQS")
COLL_SEGMENTS = os.getenv("COLL_SEGMENTS")
COLL_POLLING  = os.getenv("COLL_POLLING")
GROQ_API_KEY  = os.getenv("GROQ_API_KEY")

client = MongoClient(MONGO_URI)
db     = client[MONGO_DB]

mcqs_col     = db[COLL_MCQS]
segments_col = db[COLL_SEGMENTS]
polling_col  = db[COLL_POLLING]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        


whisper_model = WhisperModel("small", device="cpu", compute_type="int8")
llm= ChatOllama(model="mistral:latest", max_tokens=200, temperature=0.2, stop=["</Lecture Excerpt>"])

async def chunk_by_window(segments, window=300.0):
    chunks = []
    current_text = []
    current_window_start = 0.0
    current_window_end   = window

    for seg in segments:
        if seg.start >= current_window_end:
            chunks.append(" ".join(current_text).strip())
            # await manager.send_progress({"id": "transcribe",   "progress": 90  })
 
            current_text = []
            while seg.start >= current_window_end:
                current_window_start += window
                current_window_end   += window
        current_text.append(seg.text)

    if current_text:
        chunks.append(" ".join(current_text).strip())

    return chunks


def generate_mcq(llm, text_chunk: str) -> str:
    # prompt = textwrap.dedent(f"""
    # You are an educational assistant. Given the following lecture excerpt, generate  multiple-choice questions (MCQ) with four options (A–D) and indicate the correct option at the end.

    # <Lecture Excerpt>
    # {text_chunk}
    # </Lecture Excerpt>

    # MCQ:
    # """).strip()
    prompt = textwrap.dedent(f"""
You are an educational assistant. Given the following lecture excerpt, generate multiple-choice questions (MCQs) in the following **JSON format**, matching the structure required by the frontend application:

<Lecture Excerpt>
{text_chunk}
</Lecture Excerpt>

Return your response as a valid JSON array like this:

[
  {{
    "question": "What is ...?",
    "options": [
      {{ "id": "a", "text": "Option A", "isCorrect": false }},
      {{ "id": "b", "text": "Option B", "isCorrect": true }},
      {{ "id": "c", "text": "Option C", "isCorrect": false }},
      {{ "id": "d", "text": "Option D", "isCorrect": false }}
    ],
    "explanation": "Short explanation of correct answer."
    }}
    ]

    Only return the array. Do not include extra text.
    """).strip()

    resp = llm.invoke(prompt)
    print("LLM response:", resp)
    return resp.content

async def format_timestamp(seconds: int) -> str:
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02}"

@app.post("/upload")
async def upload_and_process(path_name:str="my.mp4"):
    # path_name="my.mp4"
    await asyncio.sleep(30)  # Simulate some processing
    await manager.send_progress({"step": "upload",   "progress": 50  })
    await manager.send_progress({"step": "upload",   "progress": 100 })
    await manager.send_progress({"step": "transcribe",   "progress": 10  })
    await asyncio.sleep(5)  # Simulate some processing
    start=datetime.now()
    video_path = f"VIDEO_FOLDER/{path_name}"
    # with open(video_path, "wb") as f:
    #     f.write(await file.read())

    file_id = int(datetime.utcnow().timestamp())
    polling_id = file_id
    insert_polling(polling_id, file_id, 0.0)

    update_polling_percentage(polling_id, 10.0)
    segments, _ = whisper_model.transcribe(video_path, language="en", beam_size=5,log_progress=True)
    # os.remove(video_path)

    await manager.send_progress({"step": "transcribe",   "progress": 50  })

    update_polling_percentage(polling_id, 30.0)
    await asyncio.sleep(5)
    chunks = await chunk_by_window(segments, window=300.0)
    await manager.send_progress({"step": "transcribe",   "progress": 90  })

    update_polling_percentage(polling_id, 50.0)

    start_time=0
    end_time=300 #secs
    mcq_counter=1
    for idx, chunk in enumerate(chunks):
        segment_id = file_id * 100 + idx
        mcqs_id = file_id * 10000 + idx
        await asyncio.sleep(5)  # Simulate processing time for each segment
        await manager.send_progress({"step": "transcribe",   "progress": 100  })
        insert_segment(file_id, segment_id, chunk)
        await manager.send_progress({"step":"segment","progress":  (idx / len(chunks)) * 100})
        await asyncio.sleep(5)  # Simulate processing time for each segment
        st=await format_timestamp(start_time)
        ft=await format_timestamp(end_time)
        time_stamp = f"{st} - {ft}"
        await manager.send_progress({"segments":{"id": segment_id, "text": chunk,"startTime": start_time, "endTime": end_time,"timestamp":time_stamp}})
        print(f"inserted segment{idx} with id", segment_id)

        try:
            mcq_text = generate_mcq(llm, chunk)
            print("Generated MCQ text:", mcq_text)
            mcq_list = json.loads(mcq_text)
            cnt1=len(chunks)*len(mcq_list)
            print("cnt1 is", cnt1)
            print("len of chunks is", len(chunks), "len of mcq_list is", len(mcq_list))
            await manager.send_progress({"step":"segment","progress":  (idx+1 / len(chunks)) * 100})
            for mcq in mcq_list:
                mcq["id"] = str(mcq_counter)
                print("index is",idx)
                mcq["segmentId"] = str(idx)
                print("mcq counter is", mcq_counter)
                await manager.send_progress({"step": "generate","progress": (mcq_counter/cnt1) * 100})
                await manager.send_progress({"mcqs":mcq})
                mcq_counter += 1

            # Insert each MCQ individually (or batch store if needed)
            insert_mcqs(file_id, segment_id, mcq_counter, mcq)
            print(f"inserted mcq {mcq['id']} for segment {segment_id}")
            
        except Exception as e:
            mcq_text = f"[Error generating question: {e}]"

        insert_mcqs(file_id, segment_id, mcqs_id, mcq_text)
        print("inserted mcqs", mcq_text)
        print(f"inserted mcq{idx} with id", mcqs_id)
        update_polling_percentage(polling_id, 50.0 + (idx / len(chunks)) * 40)
        await asyncio.sleep(5)  # Simulate processing time for each segment
        # print(f"updated polling percentage to {50.0 + (idx / len(chunks)) * 40}")

    update_polling_percentage(polling_id, 100.0)
    # await manager.send_progress({"step": "generate","progress": 10})
    await asyncio.sleep(5)
    await manager.send_progress({"step": "generate","progress": 100})
    
    end = datetime.now()
    print("total time taken:", end - start) 
    duration = end - start
    total_seconds = duration.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    await manager.send_progress({"step": "generate","done": 100})

    print(f"Total time: {minutes} min {seconds} sec")
    return {"file_id": file_id, "segments_processed": len(chunks)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("python_fastapi:app", host="127.0.0.1", port=8002, reload=True)












# @app.get("/get-mcq/{file_id}/{segment_id}")
# def get_mcq(file_id: int, segment_id: int):
#     return get_mcqs(file_id, segment_id)

# @app.get("/get-segment/{file_id}/{segment_id}")
# def get_segment_text(file_id: int, segment_id: int):
#     return get_segment(file_id, segment_id)

# @app.get("/polling/{polling_id}")
# def get_polling_status(polling_id: int):
#     data = polling_col.find_one({"polling_id": polling_id}, {"_id": 0})
#     return {"percentage": data.get("percentage", 0.0)} if data else {"percentage": 0.0}


# def insert_segment(file_id: int, segment_id: int, text: str) -> str:
#     return str(segments_col.insert_one({
#         "file_id": file_id,
#         "segment_id": segment_id,
#         "segments_text": text
#     }).inserted_id)

# def insert_mcqs(file_id: int, segment_id: int, mcqs_id: int, mcqs_text: str) -> str:
#     return str(mcqs_col.insert_one({
#         "mcqs_id": mcqs_id,
#         "file_id": file_id,
#         "segment_id": segment_id,
#         "mcqs": mcqs_text
#     }).inserted_id)

# def insert_polling(polling_id: int, file_id: int, percentage: float) -> str:
#     return str(polling_col.insert_one({
#         "polling_id": polling_id,
#         "file_id": file_id,
#         "percentage": percentage
#     }).inserted_id)

# def update_polling_percentage(polling_id: int, new_percentage: float) -> int:
#     result = polling_col.update_one(
#         {"polling_id": polling_id},
#         {"$set": {"percentage": new_percentage}}
#     )
#     return result.modified_count

# def get_mcqs(file_id:int, segment_id: int) -> Dict[str, Any]:
#     return mcqs_col.find_one({"file_id": file_id, "segment_id": segment_id}, {"_id": 0})

# def get_segment(file_id: int, segment_id: int) -> Dict[str, Any]:
#     return segments_col.find_one({"file_id": file_id, "segment_id": segment_id}, {"_id": 0})
