from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

# colunas = Gender,RaceEthnicity,ParentalLevelEducation,Lunch,TestPreparation,ReadingScore,WritingScore,Outcome

class Aluno(Base):
    __tablename__ = 'alunos'
    
    id = Column(Integer, primary_key=True)
    name = Column("name", String(50))
    gender = Column("gender", Integer)
    race_ethnicity = Column("race_ethnicity", Integer)
    parental_level_education = Column("parental_level_education", Integer)
    lunch = Column("lunch", Integer)
    test_preparation = Column("test_preparation", Integer)
    reading_score = Column("reading_score", Integer)
    writing_score = Column("writing_score", Integer)
    outcome = Column("outcome", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self, name:str, gender:int, race_ethnicity:int, 
                 parental_level_education:int, lunch:int, test_preparation:int,
                 reading_score:int, writing_score:int, outcome:int, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Aluno

        Arguments:
            name: nome do aluno
            gender: O gênero do aluno (masculino/feminino)
            race_ethnicity: Origem racial ou étnica do aluno (asiático, afro-americano, hispânico, etc...)
            parental_level_education: O mais alto nível de escolaridade alcançado pelos pais ou responsáveis ​​do aluno
            lunch: Se o aluno recebe almoço grátis ou com preço reduzido (sim/não)
            test_preparation: Se o aluno concluiu um curso de preparação para testes (sim/não)
            reading_score: A pontuação do aluno em um teste de leitura padronizado
            writing_score: A pontuação do aluno em um teste de redação padronizado
            outcome: diagnóstico
            data_insercao: data de quando o aluno foi inserido à base
        """
        self.name = name
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_education = parental_level_education
        self.lunch = lunch
        self.test_preparation = test_preparation
        self.reading_score = reading_score
        self.writing_score = writing_score
        self.outcome = outcome

        # se não for informada, será a data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao