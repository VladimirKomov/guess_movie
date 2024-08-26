function startGame() {
    // Clear all previous hints and result
    document.getElementById("hint1").style.display = "none";
    document.getElementById("hint2").style.display = "none";
    document.getElementById("hint3").style.display = "none";
    document.getElementById("hint4").style.display = "none";
    document.getElementById("hint5").style.display = "none";
    document.getElementById("hint-image").style.display = "none";
    document.getElementById("answer").value = "";
    document.getElementById("result").textContent = "";
    document.getElementById("hint2-btn").style.display = "none";
    document.getElementById("hint3-btn").style.display = "none";
    document.getElementById("hint4-btn").style.display = "none";
    document.getElementById("hint5-btn").style.display = "none";
    document.getElementById("hint6-btn").style.display = "none";
    document.getElementById("reveal-answer-btn").style.display = "none";

    // Enable the answer input and check button
    document.getElementById("answer").disabled = false;
    document.getElementById("check-answer-btn").disabled = false;

    // Start a new game
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
              if (hintNumber < 6) {
                  // Display the hint and prepare the next button
                  document.getElementById(`hint${hintNumber}`).textContent = data.hint;
                  document.getElementById(`hint${hintNumber}`).style.display = "block";
                  document.getElementById(`hint${hintNumber}-btn`).disabled = true;

                  if (hintNumber + 1 <= 6) {
                      document.getElementById(`hint${hintNumber + 1}-btn`).style.display = "inline-block";
                  } else {
                      document.getElementById("reveal-answer-btn").style.display = "inline-block";
                  }
              } else if (hintNumber === 6) {  // Image hint
                  const imageUrl = data.hint;
                  document.getElementById("hint-image").src = imageUrl;
                  document.getElementById("image-link").href = imageUrl;
                  document.getElementById("image-hint").style.display = "block";
                  document.getElementById(`hint${hintNumber}-btn`).disabled = true;
                  document.getElementById("reveal-answer-btn").style.display = "inline-block";
              }
          }
      });
}

function revealAnswer() {
    // Disable the button after it is clicked
    document.getElementById("reveal-answer-btn").disabled = true;
    fetch('/reveal_answer', {
        method: 'POST'
    }).then(response => response.json())
      .then(data => {
          if (data.poster_url) {
              // Display the answer image
              document.getElementById("answer-image").src = data.poster_url;
              document.getElementById("answer-poster").style.display = "block";

              // Disable the answer input and check button
              document.getElementById("answer").disabled = true;
              document.getElementById("check-answer-btn").disabled = true;
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
          // Display the result of the answer check
          resultElement.textContent = data.result;
          resultElement.style.color = data.correct ? "green" : "red";
      });
}

function endAndStartNewGame() {
    fetch('/end_game', {
        method: 'POST'
    }).then(response => response.json())
      .then(data => {
          if (data.status === 'Game ended') {
              // Start a new game and refresh the page
              startGame();
              window.location.reload(); // Reload the page after starting a new game
          }
      });
}
