from fastapi import APIRouter, HTTPException, status, Response, Depends

router = APIRouter(tags=['Kitchen'], prefix='/api/v1/kitchen')