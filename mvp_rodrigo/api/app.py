from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Aluno, Model
from logger import logger
from schemas import *
from flask_cors import CORS

# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
aluno_tag = Tag(name="Aluno", description="Adição, visualização, remoção e predição sobre análise de alunos")

# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# Rota de listagem de alunos
@app.get('/alunos', tags=[aluno_tag],
         responses={"200": AlunoViewSchema, "404": ErrorSchema})
def get_alunos():
    """Lista todos os alunos cadastrados na base
    Retorna uma lista de alunos cadastrados na base.
    
    Args:
        nome (str): nome do aluno
        
    Returns:
        list: lista de alunos cadastrados na base
    """
    session = Session()
    
    # Buscando todos os alunos
    alunos = session.query(Aluno).all()
    
    if not alunos:
        logger.warning("Não há alunos cadastrados na base :/")
        return {"message": "Não há alunos cadastrados na base :/"}, 404
    else:
        logger.debug(f"%d alunos econtrados" % len(alunos))
        return apresenta_alunos(alunos), 200


# Rota de adição de aluno
@app.post('/aluno', tags=[aluno_tag],
          responses={"200": AlunoViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: AlunoSchema):
    """Adiciona um novo aluno à base de dados
    Retorna uma representação dos alunos e diagnósticos associados.
    
    Args:
        name (str): nome do aluno
        gender (int): O gênero do aluno (masculino/feminino)
        race_ethnicity (int): Origem racial ou étnica do aluno (asiático, afro-americano, hispânico, etc...)
        parental_level_education (int): O mais alto nível de escolaridade alcançado pelos pais ou responsáveis ​​do aluno
        lunch (int): Se o aluno recebe almoço grátis ou com preço reduzido (sim/não)
        test_preparation (int): Se o aluno concluiu um curso de preparação para testes (sim/não)
        reading_score (int): A pontuação do aluno em um teste de leitura padronizado
        writing_score (int): A pontuação do aluno em um teste de redação padronizado
        
    Returns:
        dict: representação do aluno e diagnóstico associado
    """
    
    # Carregando modelo
    ml_path = 'ml_model/modelo_treinado.pkl'
    logger.debug("Tentando carregar modelo...")
    modelo = Model.carrega_modelo(ml_path)

    #print(f"nome: {form.name.strip()} \ngender: {form.gender} \nrace_ethnicity: {form.race_ethnicity} \nparental_level_education: {form.parental_level_education} \nlunch: {form.lunch} \ntest_preparation: {form.test_preparation} \nreading_score: {form.reading_score} \nwriting_score: {form.writing_score}")
    
    aluno = Aluno(
        name = form.name.strip(),
        gender = form.gender,
        race_ethnicity = form.race_ethnicity,
        parental_level_education = form.parental_level_education,
        lunch = form.lunch,
        test_preparation = form.test_preparation,
        reading_score = form.reading_score,
        writing_score = form.writing_score,
        outcome=Model.preditor(modelo, form)
    )
    logger.debug(f"Adicionando produto de nome: '{aluno.name}'")

    print(aluno)
    
    try:
        # Criando conexão com a base
        session = Session()
        logger.debug("Conexão com a base de dados realizada.")
        
        # Checando se aluno já existe na base
        logger.debug("Checando se aluno já existe na base")
        if session.query(Aluno).filter(Aluno.name == form.name).first():
            error_msg = "Aluno já existente na base :/"
            logger.warning(f"Erro ao adicionar aluno '{aluno.name}', {error_msg}")
            return {"message": error_msg}, 409
        
        # Adicionando aluno
        logger.debug(f"Adicionando aluno de nome: '{aluno.name}'")
        session.add(aluno)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado aluno de nome: '{aluno.name}'")
        return apresenta_aluno(aluno), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar aluno '{aluno.name}', {error_msg}")
        return {"message": error_msg}, 400
    

# Métodos baseados em nome
# Rota de busca de aluno por nome
@app.get('/aluno', tags=[aluno_tag],
         responses={"200": AlunoViewSchema, "404": ErrorSchema})
def get_aluno(query: AlunoBuscaSchema):    
    """Faz a busca por um aluno cadastrado na base a partir do nome

    Args:
        nome (str): nome do aluno
        
    Returns:
        dict: representação do aluno e diagnóstico associado
    """
    
    aluno_nome = query.name
    logger.debug(f"Coletando dados sobre produto #{aluno_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    aluno = session.query(Aluno).filter(Aluno.name == aluno_nome).first()
    
    if not aluno:
        # se o aluno não foi encontrado
        error_msg = f"Aluno {aluno_nome} não encontrado na base :/"
        logger.warning(f"Erro ao buscar produto '{aluno_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Aluno econtrado: '{aluno.name}'")
        # retorna a representação do aluno
        return apresenta_aluno(aluno), 200
   
    
# Rota de remoção de aluno por nome
@app.delete('/aluno', tags=[aluno_tag],
            responses={"200": AlunoViewSchema, "404": ErrorSchema})
def delete_aluno(query: AlunoBuscaSchema):
    """Remove um aluno cadastrado na base a partir do nome

    Args:
        nome (str): nome do aluno
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    
    aluno_nome = unquote(query.name)
    logger.debug(f"Deletando dados sobre aluno #{aluno_nome}")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando aluno
    aluno = session.query(Aluno).filter(Aluno.name == aluno_nome).first()
    
    if not aluno:
        error_msg = "Aluno não encontrado na base :/"
        logger.warning(f"Erro ao deletar aluno '{aluno_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(aluno)
        session.commit()
        logger.debug(f"Deletado aluno #{aluno_nome}")
        return {"message": f"Aluno {aluno_nome} removido com sucesso!"}, 200