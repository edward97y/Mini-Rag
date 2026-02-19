from fastapi import Request,APIRouter,status
from fastapi.responses import JSONResponse
import logging
from .schemes.nlp import PushRequest,SearchRequest
from models import ProjectModel,ChunkModel
from models.enums.ResponseEnums import ResponseSignal
from controllers import NLPController
logger=logging.getLogger("uvicorn.error")


nlp_router=APIRouter(prefix="/api/v1/nlp",
                     tags=["api_v1","nlp"])

@nlp_router.post("/index/push/{project_id}")
async def index_project(request:Request,project_id:str,push_request:PushRequest):
    project_model=await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    project=await project_model.get_project_or_create_one(project_id=project_id)

    if not project:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.PROJECT_NOT_FOUND_ERROR.value})
    
    nlp_controller=NLPController(vector_db_client=request.app.vector_db_client,
                                 embed_client=request.app.embed_client,
                                 generation_client=request.app.generation_client,
                                template_parser=request.app.template_parser)
    
    chunk_model=await ChunkModel.create_instance(db_client=request.app.db_client)

    has_record=True
    page_no=1
    inserted_item_count=0
    idx = 0
    while has_record:
        page_chunks = await chunk_model.get_chunk_by_project_id(project_id=project.id, page_no=page_no)

        if len(page_chunks):
            
            page_no += 1
            inserted_item_count+=len(page_chunks)
        
        if not page_chunks or len(page_chunks) == 0:
            has_record = False
            break
        
        
        chunks_ids=list(range(idx,idx+len(page_chunks)))
        is_inserted= nlp_controller.index_into_vector_db(project=project,chunks=page_chunks,do_reset=push_request.do_reset,chunks_ids=chunks_ids)

        
        
        
 
    

    if not is_inserted:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.INSERT_INTO_VECTOR_DB_ERROR.value})
    
    
    return JSONResponse(status_code=status.HTTP_200_OK
                        ,content={"signal":ResponseSignal.INSERT_INTO_VECTOR_DB_SUCCESS.value,"inserted_item_count":inserted_item_count})

@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request:Request,project_id:str):
    project_model=await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    project=await project_model.get_project_or_create_one(project_id=project_id)

    nlp_controller=NLPController(vector_db_client=request.app.vector_db_client,
                                 embed_client=request.app.embed_client,
                                 generation_client=request.app.generation_client,
                                template_parser=request.app.template_parser)

    collection_info=nlp_controller.get_vector_db_collection(project=project)

    return JSONResponse(status_code=status.HTTP_200_OK
                        ,content={"signal":ResponseSignal.VECTOR_COLLECTION_RETRIVED.value,"collection_info":collection_info}) 
    

@nlp_router.post("/index/search/{project_id}")
async def search_index(request:Request,project_id:str,search_request:SearchRequest):
    project_model=await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    project=await project_model.get_project_or_create_one(project_id=project_id)

    nlp_controller=NLPController(vector_db_client=request.app.vector_db_client,
                                 embed_client=request.app.embed_client,
                                 generation_client=request.app.generation_client,
                                 template_parser=request.app.template_parser)
    
    results=nlp_controller.search_vector_db_collection(project=project,text=search_request.text,limit=search_request.limit)
    
    if not results:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.VECTOR_DB_SEARCH_ERROR.value})


    points=results.points
    
    result={"text":points[0].payload["text"],"score":points[0].score}
    return JSONResponse(status_code=status.HTTP_200_OK
                        ,content={"signal":ResponseSignal.VECTOR_DB_SEARCH_SUCCESS.value,"result":result})
 
    
@nlp_router.post("/index/answer{project_id}")
async def search_index(request:Request,project_id:str,search_request:SearchRequest):
    project_model=await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    project=await project_model.get_project_or_create_one(project_id=project_id)

    nlp_controller=NLPController(vector_db_client=request.app.vector_db_client,
                                 embed_client=request.app.embed_client,
                                 generation_client=request.app.generation_client,
                                 template_parser=request.app.template_parser)
    answer,full_prompt,chat_history=nlp_controller.answer_rag_question(project=project,query=search_request.text,limit=search_request.limit)

    if not answer:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.RAG_ANSWER_ERROR.value})
    return JSONResponse(content={"signal":ResponseSignal.RAG_ANSWER_SUCCESS.value,"answer":answer,"full_prompt":full_prompt,"chat_history":str(chat_history)})
    

