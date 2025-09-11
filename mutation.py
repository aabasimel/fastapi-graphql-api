import strawberry
from service.note import NoteService
from schema import NoteType, NoteInput


@strawberry.type
class DeleteResult:
    success: bool
    message: str

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def createNote(self, note_data:NoteInput)->NoteType:
        return await NoteService.add_note(note_data)
    @strawberry.mutation
    async def update_note(self,note_id:int,note_data:NoteInput)->str:
        return await NoteService.update_note(note_id,note_data)
    
    @strawberry.mutation
    async def delete_note(self, note_id:int)->DeleteResult:
        try:
            return DeleteResult(success=True, message=f'successfully deleted note')
        except Exception as e:
            return DeleteResult(success=False, message=str(e))

        return await NoteService.delete_note(note_id)
    
    
