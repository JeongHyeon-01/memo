from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId


app = FastAPI()

# mongo 연결 테스트
try:
    client = MongoClient("mongodb://localhost:27017")
    db = client["memo_app"]  # 데이터베이스 이름
    memos_collection = db["memos"]  # 컬렉션 이름
    print("connect")
except Exception as e:
    print(f"MongoDB 연결 실패: {e}")

#모델 정의
class Memo(BaseModel):
    content : str
    
    
#CRUD구현
@app.post('/memos')
def create_memo(memo:Memo): 
    new_memo = {"content": memo.content}
    result = memos_collection.insert_one(new_memo)
    return {"id": str(result.inserted_id), "message": "메모가 생성되었습니다."}

@app.get('/memos')
def get_memo():
    memos = []
    for memo in memos_collection.find():
        memos.append({"id": str(memo["_id"]), "content": memo["content"]})
    return memos

@app.put('/memo/{memo_id}')
def put_memo(memo_id: str, memo: Memo):
    result = memos_collection.update_one(
        {"_id": ObjectId(memo_id)}, {"$set": {"content": memo.content}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")
    return {"message": "메모가 업데이트되었습니다."}

@app.delete("/memo/{memo_id}")
def delete_memo(memo_id: str):
    result = memos_collection.delete_one({"_id": ObjectId(memo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")
    return {"message": "메모가 삭제되었습니다."}
            

app.mount("/", StaticFiles(directory="static", html=True), name="static")