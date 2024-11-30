from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

class Memo(BaseModel):
    id  : str
    content : str

memos =[]

app = FastAPI()

@app.post('/memos')
def create_memo(memo:Memo): 
    memos.append(memo)
    return '성공했습니다.'


@app.get('/memos')
def get_memo():
    return memos

@app.put('/memo/{memo_id}')
def put_memo(req_memo:Memo):
    for i in memos:
        if i.id  == req_memo.id:
            i.content = req_memo.content
            return '성공'
    return "실패"

@app.delete('/memo/{memo_id}')
def delete_memo(memo_id):
    # for i in memos:
    #     if i.id == memo_id:
    #         memos.remove(i)
    for idx, memo in enumerate(memos):
        if memo.id == memo_id:
            memos.pop(idx)
            

app.mount("/", StaticFiles(directory='static', html=True), name="static")