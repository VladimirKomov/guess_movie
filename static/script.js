function checkAnswer() {
    const answer = document.getElementById("answer").value;

    fetch('/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `answer=${encodeURIComponent(answer)}`
    })
    .then(response => response.json())
    .then(data => {
        const resultElement = document.getElementById("result");
        resultElement.textContent = data.result;
        resultElement.style.color = data.result === "Correct!" ? "green" : "red";
    });
}
