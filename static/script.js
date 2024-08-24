function startGame() {
    // Очистка всех предыдущих подсказок и результата
    document.getElementById("hint1").style.display = "none";
    document.getElementById("hint2").style.display = "none";
    document.getElementById("hint-image").style.display = "none";
    document.getElementById("answer").value = "";
    document.getElementById("result").textContent = "";
    document.getElementById("hint2-btn").style.display = "none";

    // Запуск новой игры
    fetch('/start_game', {
        method: 'POST'
    }).then(response => response.json())
      .then(data => {
          if (data.game_started) {
              document.getElementById("hint1").textContent = data.hints.keywords;
              document.getElementById("hint1").style.display = "block";
              document.getElementById("hint2-btn").style.display = "inline-block";
          }
      });
}

function showHint(hintNumber) {
    fetch('/get_hint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `hint_number=${hintNumber}`
    }).then(response => response.json())
      .then(data => {
          if (data.hint) {
              if (hintNumber < 5) {
                  document.getElementById(`hint${hintNumber}`).textContent = data.hint;
                  document.getElementById(`hint${hintNumber}`).style.display = "block";
                  document.getElementById(`hint${hintNumber + 1}-btn`).style.display = "inline-block";
              } else if (hintNumber === 5) {
                  // Если это последняя подсказка (картинка)
                  document.getElementById("hint-image").src = data.hint;
                  document.getElementById("hint-image").style.display = "block";
              }
          }
      });
}

function endAndStartNewGame() {
    fetch('/end_game', {
        method: 'POST'
    }).then(response => response.json())
      .then(data => {
          if (data.status === 'Game ended') {
              startGame();  // Запускаем новую игру после завершения предыдущей
          }
      });
}

function checkAnswer() {
    const userAnswer = document.getElementById("answer").value;

    fetch('/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `answer=${encodeURIComponent(userAnswer)}`
    }).then(response => response.json())
      .then(data => {
          const resultElement = document.getElementById("result");
          resultElement.textContent = data.result;
          resultElement.style.color = data.correct ? "green" : "red";
      });
}

