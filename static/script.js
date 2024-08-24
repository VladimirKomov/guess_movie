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
              document.getElementById(`hint${hintNumber}`).innerHTML = data.hint;
              document.getElementById(`hint${hintNumber}`).style.display = "block";
              if (hintNumber < 6) {
                  document.getElementById(`hint${hintNumber + 1}-btn`).style.display = "inline-block";
              }
          }
      });
}

function startGame() {
    fetch('/start_game', {
        method: 'POST'
    }).then(response => response.json())
      .then(data => {
          if (data.game_started) {
              document.getElementById("game-area").innerHTML = `
                  <p id="hint1" class="hint">${data.hints.keywords}</p>
                  <button id="hint2-btn" onclick="showHint(2)">Get Second Hint</button>
                  <p id="hint2" class="hint" style="display:none;"></p>
                  
                  <button id="hint3-btn" onclick="showHint(3)" style="display:none;">Get Third Hint</button>
                  <p id="hint3" class="hint" style="display:none;"></p>
                  
                  <button id="hint4-btn" onclick="showHint(4)" style="display:none;">Get Fourth Hint</button>
                  <p id="hint4" class="hint" style="display:none;"></p>
                  
                  <button id="hint5-btn" onclick="showHint(5)" style="display:none;">Get Fifth Hint</button>
                  <p id="hint5" class="hint" style="display:none;"></p>
                  
                  <button id="hint6-btn" onclick="showHint(6)" style="display:none;">Get Final Hint</button>
                  <p id="hint6" class="hint" style="display:none;"></p>
                  
                  <input type="text" id="answer" placeholder="Enter your guess...">
                  <button onclick="checkAnswer()">Check Answer</button>
                  <p id="result"></p>
              `;
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

