from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes import auth, user
from schemas import CustomValidationErrorResponse, ValidationErrorDetail

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    # Custom validation format
    errors = [
        ValidationErrorDetail(
            field = err['loc'][-1],
            message = err['msg']
        )

        for err in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content=CustomValidationErrorResponse(errors = errors).dict()
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router)
app.include_router(user.router)

@app.get('/')
def root():
    return { 'message': 'Hi!' }
