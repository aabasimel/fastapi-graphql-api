from fastapi import FastAPI
import uvicorn
from config import db
from Graphql.mutation import Mutation
from Graphql.query import Query
from strawberry.fastapi import GraphQLRouter
import strawberry
from fastapi.middleware.cors import CORSMiddleware

def init_app():
    apps = FastAPI(
        title="example",
        description="Fast API",
        version="1.0.0"
    )
    
    # Add CORS middleware here
    apps.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins (for development only)
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    @apps.on_event("startup")
    async def startup():
        await db.create_all()
    
    @apps.on_event("shutdown")
    async def shutdown():
        await db.close()
   
    @apps.get("/")
    def home():
        return {"welcome": "to fastapi"}
    
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    apps.include_router(GraphQLRouter(schema=schema), prefix="/graphql", tags=["graphql"])
    
    return apps

app = init_app()

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="localhost", port=8000, reload=True)