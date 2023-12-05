from pydantic import BaseModel
from typing import Optional, List
from model.aluno import Aluno
import json
import numpy as np

class AlunoSchema(BaseModel):
    """ Define como um novo aluno a ser inserido deve ser representado
    """
    name: str = "Rodrigo"
    gender: int = 1
    race_ethnicity: int = 2
    parental_level_education: int = 1
    lunch: int = 1
    test_preparation: int = 0
    reading_score: int = 85
    writing_score: int = 78
    
class AlunoViewSchema(BaseModel):
    """Define como um aluno será retornado
    """
    id: int = 1
    name: str = "Rodrigo"
    gender: int = 1
    race_ethnicity: int = 2
    parental_level_education: int = 1
    lunch: int = 1
    test_preparation: int = 0
    reading_score: int = 85
    writing_score: int = 78
    outcome: int = None
    
class AlunoBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do aluno.
    """
    name: str = "Rodrigo"

class ListaAlunosSchema(BaseModel):
    """Define como uma lista de alunos será representada
    """
    alunos: List[AlunoSchema]

    
class AlunoDelSchema(BaseModel):
    """Define como um aluno para exclusão será representado
    """
    name: str = "Rodrigo"
    
# Apresenta apenas os dados de um aluno    
def apresenta_aluno(aluno: Aluno):
    """ Retorna uma representação do aluno seguindo o schema definido em
        AlunoViewSchema.
    """
    return {
        "id": aluno.id,
        "name": aluno.name,
        "gender": aluno.gender,
        "race_ethnicity": aluno.race_ethnicity,
        "parental_level_education": aluno.parental_level_education,
        "lunch": aluno.lunch,
        "test_preparation": aluno.test_preparation,
        "reading_score": aluno.reading_score,
        "writing_score": aluno.writing_score,
        "outcome": aluno.outcome
    }
    
# Apresenta uma lista de alunos
def apresenta_alunos(alunos: List[Aluno]):
    """ Retorna uma representação do aluno seguindo o schema definido em
        AlunoViewSchema.
    """
    result = []
    for aluno in alunos:
        result.append({
            "id": aluno.id,
            "name": aluno.name,
            "gender": aluno.gender,
            "race_ethnicity": aluno.race_ethnicity,
            "parental_level_education": aluno.parental_level_education,
            "lunch": aluno.lunch,
            "test_preparation": aluno.test_preparation,
            "reading_score": aluno.reading_score,
            "writing_score": aluno.writing_score,
            "outcome": aluno.outcome
        })

    return {"alunos": result}

