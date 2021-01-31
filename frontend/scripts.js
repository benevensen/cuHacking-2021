let ctr = 0;

function remove(el) {
    let element = el;
    element.classList.add("hidden");
    element.remove();
}

function checkAnswer(el) {

}

function getAuth(entry_code) {
    fetch("http://localhost:8081/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "event_id": entry_code
        }),
    })
        .then(res => res.json())
        .then((data) => {
            localStorage.setItem("auth_code", data["token"])
        })
}

function newQuestion(bearer) {
    fetch("http://localhost:8081/quest/approved", {
        method: "GET",
        headers: {
            "Authorization: Bearer": bearer
        }
    })
        .then(res => res.json())
        .then((data) => {
            localStorage.setItem('question', data['question'])
        })
}

function submitQuestion(bearer, text_ans) {
    fetch("http://localhost:8081/quest/approved", {
        method: "POST",
        headers: {
            "Authorization: Bearer": bearer
        },
        body: {
            "answer": text_ans
        },
    })
        .then(res => res.json())
}
