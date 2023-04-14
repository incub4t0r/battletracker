from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
import json
from database import Database
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

db = Database('store.db')
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewChallenge(BaseModel):
    name: str
class Challenge(BaseModel):
    id: str
    name: str
    member: str
    completed: bool
    flag: str

class NewMember(BaseModel):
    name: str

class Member(BaseModel):
    name: str
    id: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

########################################################################
# Challenges
########################################################################

@app.get("/challenges")
async def read_challenges():
    results = db.fetchall_challenge()
    json_results = []
    for result in results:
        json_results.append({
            "id": result[0],
            "name": result[1],
            "member": result[2],
            "start_time": result[3],
            "checkin_time": result[4],
            "completed": result[5],
            "flag": result[6]
        })
    print(json.dumps(json_results))
    return json_results

@app.post("/challenges")
async def create_item(new_challenge: NewChallenge):
    start_time = datetime.now().strftime("%H%M")
    checkin_time = (datetime.now() + timedelta(minutes=30)).strftime("%H%M")
    unique_id = str(uuid4())
    db.insert_challenge(unique_id, new_challenge.name, "None", start_time, checkin_time, "")
    return {"challenge_name": new_challenge.name, "challenge_id": unique_id}

@app.put("/challenges")
async def update_challenge(challenge: Challenge):
    db.update_challenge(challenge.id, challenge.member, challenge.completed)
    return {"challenge_name": challenge.name, "challenge_id": challenge.id, "challenge_member": challenge.member, "challenge_completed": challenge.completed}

@app.put("/challenges/flag")
async def update_flag(challenge: Challenge):
    db.update_challenge(challenge.id, challenge.member, challenge.completed)
    db.update_challenge_flag(challenge.id, challenge.flag)
    return {"challenge_name": challenge.name, "challenge_id": challenge.id, "challenge_member": challenge.member, "challenge_completed": challenge.completed}

@app.delete("/challenges")
async def delete_item(challenge: Challenge):
    print("received delete request")
    db.remove_challenge(challenge.id)
    return {"challenge_id": challenge.id + " deleted"}

########################################################################
# Members
########################################################################

@app.get("/members")
async def read_members():
    results = db.fetchall_member()
    json_results = []
    for result in results:
        json_results.append({
            "id": result[0],
            "name": result[1]
        })
    return json_results

@app.post("/members")
async def create_member(new_member: NewMember):
    unique_id = str(uuid4())
    db.insert_member(unique_id, new_member.name)
    return {"member_name": new_member.name, "member_id": unique_id}

@app.put("/members")
async def update_member(member: Member):
    db.update_member(member.id, member.name)
    return {"member_name": member.name, "member_id": member.id}

@app.delete("/members")
async def delete_member(member: Member):
    db.remove_member(member.id)
    return {"member_id": member.id + " deleted"}

def test():
    db.clear()
    class Challenge(object):
        def __init__(self, name, id):
            self.name = name
            self.id = id

    challenge_one = Challenge(name="challenge_one", id=str(uuid4())) 
    db.insert_challenge(challenge_one.id, challenge_one.name, "None", "1200", "1230", "")
    challenge_two = Challenge(name="challenge_two", id=str(uuid4()))
    db.insert_challenge(challenge_two.id, challenge_two.name, "None", "1400", "1230", "")
    challenge_three = Challenge(name="challenge_three", id=str(uuid4()))
    db.insert_challenge(challenge_three.id, challenge_three.name, "None", "1400", "1230", "")
    db.update_challenge(challenge_three.id, "the best", True)
    db.insert_member(str(uuid4()), "name1")
    db.insert_member(str(uuid4()), "name2")

if __name__ == "__main__":
    # test()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
