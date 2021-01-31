let ctr = 0;

function remove(el) {
    let element = el;
    element.classList.add("hidden");
    element.remove();
}

function checkAnswer(el) {
    let element = el;
    let value = element.getAttribute('name');
    if(value == "True"){
        ctr++; //grant a point for correct answer
        console.log(ctr);
    }
}