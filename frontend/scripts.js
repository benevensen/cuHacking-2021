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

function getQuestion(el) {
    let question;
    let title;
    fetch("http://localhost:8081/question/approved", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("auth_code")
        }
    })
        .then(res => res.json())
        .then((data) => {
            data['questions'].forEach(function (item) {
                    question = document.createElement(" <div>")
                    question.className = "wrapper bg-grey question_box"
                    title = document.createElement('<h6>')
                    title.textContent = item['prompt']
                    question.append(document.createElement('<h6>'))
                    el.append();
                }
            )
        })
}

function checkAnswer(text_ans) {
    fetch("http://localhost:8081/quest/approved", {
        method: "POST",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("auth_code")
        },
        body: {
            "answer": text_ans
        },
    })
        .then(res => res.json())
}
