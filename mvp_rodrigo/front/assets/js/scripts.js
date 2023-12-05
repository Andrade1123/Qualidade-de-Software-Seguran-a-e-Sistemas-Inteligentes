/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/alunos';
  fetch(url, {method: 'get',}
  ).then((response) => response.json()
  ).then((data) => {
      data.alunos.forEach(item => 
        insertList(
          item.name, 
          item.gender, 
          item.race_ethnicity,
          item.parental_level_education,
          item.lunch,
          item.test_preparation,
          item.reading_score,
          item.writing_score,
          item.outcome
        ))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()

/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
  */
const postItem = async (inputName, inputGender, inputRaceEthnicity, inputParentalLevelEducation, 
  inputLunch, inputTest_preparation, inputReadingScore, inputWritingScore) => {

    const formData = new FormData();
    formData.append('name', inputName);
    formData.append('gender', inputGender);
    formData.append('race_ethnicity', inputRaceEthnicity);
    formData.append('parental_level_education', inputParentalLevelEducation);
    formData.append('lunch', inputLunch);
    formData.append('test_preparation', inputTest_preparation);
    formData.append('reading_score', inputReadingScore);
    formData.append('writing_score', inputWritingScore);

    let url = 'http://127.0.0.1:5000/aluno';
    
    fetch(url, {
      method: 'post',
      body: formData
    }).then((response) => response.json())
      .catch((error) => {
        console.error('Error:', error);
      });
}

/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(nomeItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  //console.log(item)
  let url = 'http://127.0.0.1:5000/aluno?name='+item;

  fetch(url, { method: 'delete'}
  ).then((response) => response.json()
  ).catch((error) => {
      console.error('Error:', error);
  });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo aluno
  --------------------------------------------------------------------------------------
*/
const newItem = async () => {
  let inputName = document.getElementById("newInputName").value;
  let inputGender = document.getElementById("newInputGender").value;
  let inputRaceEthnicity = document.getElementById("newInputRaceEthnicity").value;
  let inputParentalLevelEducation = document.getElementById("newInputParentalLevelEducation").value;
  let inputLunch = document.getElementById("newInputLunch").value;
  let inputTestPreparation = document.getElementById("newInputTestPreparation").value;
  let inputReadingScore = document.getElementById("newInputReadingScore").value;
  let inputWritingScore = document.getElementById("newInputWritingScore").value;

  // Verifique se o aluno já existe antes de adicionar
  const checkUrl = `http://127.0.0.1:5000/alunos?nome=${inputName}`;
  fetch(checkUrl, {method: 'get'}
  ).then((response) => response.json()
  ).then((data) => {

      if (data.alunos && data.alunos.some(item => item.name === inputName)) {
        alert("O aluno já está cadastrado.\nCadastre o aluno com um nome diferente ou atualize o existente.");

      } else if (inputName === '') {
        alert("O nome do aluno não pode estar vazio!");

      } else if (isNaN(inputGender) || isNaN(inputRaceEthnicity) || isNaN(inputParentalLevelEducation) || isNaN(inputLunch) 
      || isNaN(inputTestPreparation) || isNaN(inputReadingScore) || isNaN(inputWritingScore)) {
        alert("Esse(s) campo(s) precisam ser preencidos!");

      } else {
        postItem(inputName, inputGender, inputRaceEthnicity, inputParentalLevelEducation, inputLunch, inputTestPreparation, inputReadingScore, inputWritingScore);

        // Solicitando uma nova resposta para recuperar outcome
        function getOutcome() {
          fetch(checkUrl, {method: 'get'}
          ).then((response) => response.json()
          ).then((data) => {
            const result = data.alunos.find(aluno => aluno.name === inputName);
            insertList(inputName, inputGender, inputRaceEthnicity, inputParentalLevelEducation, inputLunch, inputTestPreparation, inputReadingScore, inputWritingScore, result.outcome);
          })
        }

        setTimeout(getOutcome, 1000);
        alert("Item adicionado!")

      }

  }).catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para traduzir a lista de números inseridos para string
  --------------------------------------------------------------------------------------
*/
const translateItems = (array) => {
  items = {
    1: {
      0: "Female",
      1: "Male"
    },
    2: {
      0: "Group A",
      1: "Group B",
      2: "Group C",
      3: "Group D",
      4: "Group E"
    },
    3: {
      0: "Associate's degree",
      1: "Bachelor's degree",
      2: "High school",
      3: "Master's degree",
      4: "Some college",
      5: "Some high school"
    },
    4: {
      0: "Free/reduced ",
      1: "Standard "
    },
    5: {
      0: "Completed ",
      1: "None"
    }
  }

  Object.keys(array).forEach(i => {
    Object.keys(items).forEach(j => {
      if(i == j) {
        Object.keys(items[j]).forEach(k => {
          if(array[i] == k) {
            array[i] = items[j][k];
          }
        });
      }
    });
  });

  return array;
}

/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (name, gender, race_ethnicity, parental_level_education, lunch, test_preparation, reading_score, writing_score, outcome) => {
  var item = translateItems([name, gender, race_ethnicity, parental_level_education, lunch, test_preparation, reading_score, writing_score, outcome]);
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);

  document.getElementById("newInputName").value = "";
  document.getElementById("newInputGender").value = "title";
  document.getElementById("newInputRaceEthnicity").value = "title";
  document.getElementById("newInputParentalLevelEducation").value = "title";
  document.getElementById("newInputLunch").value = "title";
  document.getElementById("newInputTestPreparation").value = "title";
  document.getElementById("newInputReadingScore").value = "";
  document.getElementById("newInputWritingScore").value = "";

  removeElement();
}