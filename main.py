from typing import List, Optional

from fastapi import FastAPI, Body, Response, HTTPException

import people
from people import Elf, Person, Gnome


app = FastAPI()


NOT_FOUND = {"description": "Not Found"}
LOGIN_CONFLICT = {"description": "Login conflict"}


@app.post(
    "/people/elf",
    tags=["people"],
    response_model=Elf,
    responses={409: LOGIN_CONFLICT}
)
async def create_elf(
        name: str = Body(...),
        login: str = Body(...),
        password: str = Body(...)
) -> Elf:
    try:
        return people.create_elf(name, login, password)
    except people.LoginConflict:
        raise HTTPException(status_code=409)


@app.post(
    "/people/gnome",
    tags=["people"],
    response_model=Gnome,
    responses={409: LOGIN_CONFLICT}
)
async def create_gnome(
        name: str = Body(...),
        login: str = Body(...),
        password: str = Body(...)
) -> Gnome:
    try:
        return people.create_gnome(name, login, password)
    except people.LoginConflict:
        raise HTTPException(status_code=409)


@app.get("/people", tags=["people"], response_model=List[Person])
async def get_people(
        limit: int = 10,
        offset: int = 0
) -> List[Person]:
    return people.get()[offset:offset + limit]


@app.get("/person/{person_id}", tags=["people"], response_model=Person, responses={404: NOT_FOUND})
async def get_person(person_id: int) -> Optional[Person]:
    person = people.first(lambda p: p.id == person_id)
    if person:
        return person
    else:
        raise HTTPException(status_code=404)


@app.patch("/elf", tags=["people"], responses={404: NOT_FOUND})
async def update_elf(elf: Elf):
    try:
        people.update_person(elf)
    except people.PersonNotFound:
        raise HTTPException(status_code=404)


@app.patch("/gnome", tags=["people"], responses={404: NOT_FOUND})
async def update_gnome(gnome: Gnome):
    try:
        people.update_person(gnome)
    except people.PersonNotFound:
        raise HTTPException(status_code=404)

