from fastapi import APIRouter

producto=APIRouter()

@producto.get('/producto')
def hellowold():
    return "hello world producto"

