# --- INÍCIO DA CONFIGURAÇÃO DO CORS ---
# Lista de origens que podem fazer requisições para a nossa API
origins = [
    "http://localhost:3000",  # <<< ADICIONE ESTA LINHA - Essencial para o desenvolvimento local do front-end
    "https://automacoes-api.hs7hhd.easypanel.host", # É uma boa prática permitir a própria origem da API
    # "https://www.seu-frontend-em-producao.com.br", # QUANDO TIVER, adicione aqui o domínio de produção do seu front-end
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- FIM DA CONFIGURAÇÃO DO CORS ---
