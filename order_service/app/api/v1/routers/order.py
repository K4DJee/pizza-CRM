from fastapi import APIRouter, HTTPException, status, Response, Depends

router = APIRouter(tags=['Order'], prefix='/api/v1/orders')