const array_steps = window.array_steps;
const compare_indices = window.compare_indices;
const steps = window.steps;

let current_step = 0;

const next_step = document.getElementById("next-btn");
const previous_step = document.getElementById("prev-btn");
const array_container = document.getElementById("array-container");
const explanation_container = document.getElementById("explanation-container");

function show_step(step){
    const current_array = array_steps[step];
    const compared_items = compare_indices[step] || [];

    let length = current_array.length;

    const array = document.createElement("div")
    array.classList.add("bubble-sort-array", "current-step")

    for (let i = 0; i < length; i++ ){
        let array_element = document.createElement("h2")
        array_element.classList.add("bubble-sort-number")
        array_element.innerText = current_array[i];

        if (compared_items.includes(i)) {
            array_element.classList.add("highlight")    
        }

        array.appendChild(array_element)
    }

    const all_steps = array_container.querySelectorAll(".bubble-sort-array");

    array_container.appendChild(array);

    for (let i = 0; i < all_steps.length; i++) {
        if (i !== all_steps.length - 1) {
            all_steps[i].classList.remove("current-step");

            const children = all_steps[i].children;
            for (let j = 0; j < children.length; j++) {
                children[j].classList.remove("highlight");
            }
        }
    }

    while(array_container.scrollHeight > array_container.clientHeight && array_container.firstChild) {
        array_container.removeChild(array_container.firstChild);
    }

    const explanation = document.createElement("p");
    explanation.innerText = steps[step];
    explanation.classList.add("current-explanation")
    explanation_container.appendChild(explanation);

    while(explanation_container.scrollHeight > explanation_container.clientHeight && explanation_container.firstChild) {
        explanation_container.removeChild(explanation_container.firstChild);
    }

    if (step === 0) {
        previous_step.disabled = true
    } else{
        previous_step.disabled = false
    }

    if (step === array_steps.length - 1) {
        next_step.disabled = true
    } else{
        next_step.disabled = false
    }
}


previous_step.addEventListener("click", () => {
    if (current_step > 0){
        current_step--;
        show_step(current_step);
    }
})

next_step.addEventListener("click", () => {
    if (current_step < array_steps.length -1 ){
        current_step++;
        show_step(current_step);
    }
})

show_step(current_step);
