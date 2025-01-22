const questions = [
    {
        question: "What is the capital of France?",
        options: ["Berlin", "Madrid", "Paris", "Rome"],
        correctAnswer: "Paris"
    },
    {
        question: "Which language runs in a web browser?",
        options: ["Java", "C", "Python", "JavaScript"],
        correctAnswer: "JavaScript"
    },
    {
        question: "What does CSS stand for?",
        options: ["Central Style Sheets", "Cascading Style Sheets", "Cascading Simple Sheets", "Cars SUVs Sailboats"],
        correctAnswer: "Cascading Style Sheets"
    }
];

let currentQuestionIndex = 0;
let score = 0;

const questionEl = document.getElementById("question");
const optionsEl = document.getElementById("options");
const nextBtn = document.getElementById("next-btn");
const scoreContainer = document.getElementById("score-container");
const scoreEl = document.getElementById("score");
const restartBtn = document.getElementById("restart-btn");

function loadQuestion() {
    const currentQuestion = questions[currentQuestionIndex];
    questionEl.textContent = currentQuestion.question;

    optionsEl.innerHTML = "";
    currentQuestion.options.forEach(option => {
        const button = document.createElement("button");
        button.textContent = option;
        button.addEventListener("click", () => selectAnswer(option));
        optionsEl.appendChild(button);
    });
}

function selectAnswer(selectedOption) {
    const correctAnswer = questions[currentQuestionIndex].correctAnswer;

    if (selectedOption === correctAnswer) {
        score++;
    }

    nextBtn.disabled = false; // Enable the Next button
}

function showScore() {
    questionEl.textContent = "";
    optionsEl.innerHTML = "";
    nextBtn.classList.add("hidden");
    
    scoreContainer.classList.remove("hidden");
    scoreEl.textContent = `${score}/${questions.length}`;
}

function restartQuiz() {
    currentQuestionIndex = 0;
    score = 0;

    scoreContainer.classList.add("hidden");
    nextBtn.classList.remove("hidden");

    loadQuestion();
}

nextBtn.addEventListener("click", () => {
    currentQuestionIndex++;

    if (currentQuestionIndex < questions.length) {
        loadQuestion();
        nextBtn.disabled = true; // Disable the Next button until an answer is selected
    } else {
        showScore();
    }
});

restartBtn.addEventListener("click", restartQuiz);

// Initialize the quiz
loadQuestion();
nextBtn.disabled = true; // Disable the Next button initially
