from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4

from database import Database

db = Database('store.db')
app = FastAPI()

class NewChallenge(BaseModel):
    name: str
class Challenge(BaseModel):
    name: str
    id: str

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
    return db.fetchall()

@app.get("/challenges/{challenge_id}")
async def read_item(challenge_id: str):
    return {"challenge_id": challenge_id}

@app.post("/challenges/")
async def create_item(new_challenge: NewChallenge):
    unique_id = str(uuid4())
    db.insert_challenge(unique_id, new_challenge.name, "None", "None")
    return {"challenge_name": new_challenge.name, "challenge_id": unique_id}

@app.put("/challenges/{challenge_id}")
async def update_item(challenge_id: str, challenge: Challenge):
    return {"challenge_name": challenge.name, "challenge_id": challenge_id}

@app.delete("/challenges/")
# async def delete_item(challenge_id: str):
async def delete_item(challenge: Challenge):
    print("received delete request")
    db.remove_challenge(challenge.id)
    return {"challenge_id": challenge.id + " deleted"}

########################################################################
# Members
########################################################################

@app.get("/members/")
async def read_members():
    return db.fetchall_member()

# @app.get("/members/{member_id}")
# async def read_member(member_id: str):
#     return {"member_id": member_id}

@app.post("/members/")
async def create_member(new_member: NewMember):
    unique_id = str(uuid4())
    db.insert_member(unique_id, NewMember.name)
    return {"member_name": NewMember.name, "member_id": unique_id}

@app.put("/members/")
async def update_member(member: Member):
    db.update_member(member.id, member.name)
    return {"member_name": member.name, "member_id": member.id}

@app.delete("/members/")
async def delete_member(member: Member):
    db.remove_member(member.id)
    return {"member_id": member.id + " deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
