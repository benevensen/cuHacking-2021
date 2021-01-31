let ctr = 0;

function remove(el) {
    let element = el;
    element.classList.add("hidden");
    element.remove();
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
    fetch('http://localhost:8081/question/approved', {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("auth_code")
        }
    })
        .then(res => res.json())
        .then((data) => {
            data['questions'].forEach(function (item) {
                    let question = document.createElement("div");
                    question.className = "wrapper bg-grey question_box";
                    let title = document.createElement('h6');
                    title.textContent = item['prompt'];
                    title.style.borderBottom = "solid 1.5px";
                    question.append(title);
                    let span = document.createElement('span');
                    span.className = "options";
                    question.append(span);
                    item['options'].forEach(function (option) {
                        let button = document.createElement('button');
                        button.className = "option";
                        button.textContent = option;
                        button.onclick = () => this.checkAnswer(item['question_id'], option, question)
                        question.append(button);
                    })
                    el.append(question);
                }
            )
        })
}

function checkAnswer(question_id, option, question) {
    fetch('http://localhost:8081/question/approved', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("auth_code")
        },
        body: JSON.stringify({
            "question_id": question_id,
            "option": option,
        }),
    })
        .then(res => res.json())
        .then((data) => {
            console.log(data)
            remove(question)
        })
}
