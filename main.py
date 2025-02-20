import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.routers import rotas_usuario, rotas_editora, rotas_livro


app = FastAPI()


# CORS
origins = ['http://localhost:3000',
            'https://myapp.vercel.com']

app.add_middleware(CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                    )


# ROTAS EDITORA
app.include_router(rotas_editora.router)

# ROTAS USUARIO
app.include_router(rotas_usuario.router)

# ROTAS LIVROS
app.include_router(rotas_livro.router)


@app.middleware('http')
async def processamento_tempo_requisicao(request: Request, next):
    print('interceptado')
    
    response = await next(request)

    print('terminada interceptação')

    return response


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)