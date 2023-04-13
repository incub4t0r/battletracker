# Battle Tracker

This is a test internal tool for CTFs

## TODO

### Phase 1
- [X] create a CRUD 
- [X] create a non-working prototype of frontend

### Phase 2
- [X] create a working prototype of frontend

### Phase 3
- [ ] add option to import json file of users
- [ ] add local storage to keep track of user data without re-import


## Plan

- The frontend will be built and ran using svelte. The backend will be built using FastAPI.
- To communicate between the frontend and backend, there will be a REST API that is queried using the fetch protocol in javascript.
- The backend will store a sqlite database of all members and all challenges.


## SQLite Format

### Challenges

| Column Name  | Type | Description                                              |
| ------------ | ---- | -------------------------------------------------------- |
| id           | TEXT | The unique id of the challenge                           |
| name         | TEXT | The name of the challenge                                |
| member       | TEXT | the name of the member that is assigned to the challenge |
| start_time   | TEXT | The time the challenge was started                       |
| checkin_time | TEXT | The time that the challenge should be checked in         |

### Members

| Column Name | Type | Description                 |
| ----------- | ---- | --------------------------- |
| id          | TEXT | The unique id of the member |
| name        | TEXT | The name of the member      |

## REST API

### Challenges

#### GET /challenges

- Returns a list of all challenges in json format
- Request Body
  - None

#### POST /challenges

- Creates a new challenge
- Request Body
    - name
        - Name of the challenge
    - member
        - Name of the member assigned to the challenge
    - start_time
        - Time the challenge was started
- Return value
    - id
    - name
    - member
    - start_time
    - checkin_time

#### PUT /challenges

- Updates a challenge
- Request Body
    - id 
      - Unique id of the challenge
    - name
    - member
    - start_time
    - checkin_time
- Return value
    - id
    - name
    - member
    - start_time
    - checkin_time
#### DELETE /challenges

- Deletes a challenge
- Request Body
    - 

### Members

#### GET /members

- Returns a list of all members in json format
- Request Body
  - None

#### POST /members

- Creates a new member
- Request Body
  - name
    - Name of the member

- Return value
  - name
    - Name of the member
  - id
    - Generated unique id of the member

#### PUT /members

- Updates a member
- Request Body
  - name
      - Name of the member
  - id
      - Unique id of the member

#### DELETE /members

- Deletes a member
- Request Body
  - name
    - Name of the member
  - id 
    - Unique id of the member
