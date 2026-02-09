const array_steps = window.array_steps;
const compare_indices = window.compare_indices;
const steps = window.steps;

let current_step = 0;

const next_step = document.getElementById("next-btn");
const previous_step = document.getElementById("prev-btn");
const array_container = document.getElementById("array-container");
const explanation_container = document.getElementById("explanation-container");
const top_pointer = document.getElementById("top-pointer")
const middle_pointer = document.getElementById("middle-pointer")
const bottom_pointer = document.getElementById("bottom-pointer")

const removed_arrays = [];
const removed_explanations = [];

function updateButtons() {
    previous_step.disabled = current_step <= 0;
    next_step.disabled = current_step >= steps.length - 1;
}


function show_step(step){
    const current_array = array_steps[step];
    const [bottom, top, middle] = compare_indices[step] || [null, null, null];

    const previousExplanations = explanation_container.querySelectorAll(".current-explanation");
    previousExplanations.forEach(p => p.classList.remove("current-explanation"));

    const array = document.createElement("div");
    array.classList.add("binary-search-array", "current-step");

    for (let i = 0; i < current_array.length; i++){
        let array_element = document.createElement("h2");
        array_element.classList.add("binary-search-number");
        array_element.innerText = current_array[i];

        if (i === middle){
            array_element.classList.add("highlight");
        }
        else if (i === top || i === bottom){
            array_element.classList.add("highlight-pointers");
        }
        else if ((i > top || i < bottom) && (top !== null && bottom !== null)){
            array_element.classList.add("discarded")
        }

        array.appendChild(array_element);
    }

    array_container.appendChild(array);
    

    array.offsetHeight;
    array.classList.add("show");

    const all_steps = array_container.querySelectorAll(".binary-search-array");
    for (let i = 0; i < all_steps.length - 1; i++){
        all_steps[i].classList.remove("current-step");
        for (let child of all_steps[i].children){
            child.classList.remove("highlight", "highlight-top", "highlight-bottom");
        }
    }

    while(array_container.scrollHeight > array_container.clientHeight && array_container.firstChild){
        removed_arrays.push(array_container.firstChild);
        array_container.removeChild(array_container.firstChild);
    }

    const previousCurrent = explanation_container.querySelector(".current-explanation");
    if (previousCurrent) {
        previousCurrent.classList.remove("current-explanation");
    }
    
    let explanation = explanation_container.querySelector(`[data-step='${step}']`);
    if (!explanation) {
        explanation = document.createElement("p");
        explanation.innerText = steps[step];
        explanation.classList.add("explanation");
        explanation.dataset.step = step;
        explanation_container.appendChild(explanation);
    }

    explanation.classList.add("current-explanation");

    while(explanation_container.scrollHeight > explanation_container.clientHeight && explanation_container.firstChild){
        removed_explanations.push(explanation_container.firstChild);
        explanation_container.removeChild(explanation_container.firstChild);
    }

    updateButtons();
    setLabels(step);
}



function delete_step(step){
    while (removed_arrays.length > 0 && array_container.scrollHeight < array_container.clientHeight) {
        const arrayToRestore = removed_arrays.pop();
        array_container.insertBefore(arrayToRestore, array_container.firstChild);
    }

    while (removed_explanations.length > 0 && explanation_container.scrollHeight < explanation_container.clientHeight) {
        const explanationToRestore = removed_explanations.pop();
        explanation_container.insertBefore(explanationToRestore, explanation_container.firstChild);
    }

    updateButtons();
    setLabels(step);

    const all_arrays = array_container.querySelectorAll(".binary-search-array");
    if (all_arrays.length) {
        const last_array = all_arrays[all_arrays.length - 1];
        last_array.classList.remove("show", "current-step");
        last_array.classList.add("hide");

        setTimeout(() => {
            if (last_array.parentNode) last_array.parentNode.removeChild(last_array);

            const all_arrays = array_container.querySelectorAll(".binary-search-array");
            if (all_arrays.length > 0) {
                const last_array = all_arrays[all_arrays.length - 1];
                const [bottom, top, middle] = compare_indices[current_step] || [];

                last_array.classList.add("current-step");
                for (let i = 0; i < last_array.children.length; i++) {
                    const child = last_array.children[i];
                    if (middle === i){
                        child.classList.add("highlight")
                    }
                    else if (i > top || i < bottom){
                        child.classList.add("discarded")
                    }
                }
            }

            const all_explanations = explanation_container.querySelectorAll("p");
            if (all_explanations.length) {
                const last_explanation = all_explanations[all_explanations.length - 1];
                last_explanation.classList.remove("current-explanation");
                last_explanation.classList.add("hide");

                setTimeout(() => {
                    if (last_explanation.parentNode) last_explanation.parentNode.removeChild(last_explanation);

                    const all_explanations = explanation_container.querySelectorAll("p");
                    if (all_explanations.length > 0) {
                        const last_explanation = all_explanations[all_explanations.length - 1];
                        last_explanation.classList.add("current-explanation");
                    }

                    previous_step.disabled = step === 0;
                    next_step.disabled = step === array_steps.length - 1;
                }, 300);
            } else {
                previous_step.disabled = step === 0;
                next_step.disabled = current_step >= array_steps.length - 1 || current_step >= steps.length - 1;
            }
        }, 300);
    }
}



previous_step.addEventListener("click", () => {
    let prev = current_step - 1;

    while (prev >= 0 && !array_steps[prev]) {
        prev--;
    }

    if (prev >= 0){
        current_step = prev;
        delete_step(current_step);
    }
})

next_step.addEventListener("click", () => {
    let next = current_step + 1;

    while (next < array_steps.length && !array_steps[next]) {
        next++;
    }

    if (next < array_steps.length ){
        current_step = next;
        show_step(current_step);
    }
})

function animatePointer(pointer, text) {
    if (pointer.innerText === text) return;

    pointer.classList.remove("animate");
    pointer.offsetHeight;
    pointer.innerText = text;
    pointer.classList.add("animate");
}

function setLabels(step){
    const current_array = array_steps[step];
    const [bottom, top, middle] = compare_indices[step] || [null, null, null];

    if (top !== null) {
        animatePointer(top_pointer, "Top: " + current_array[top]);
    }

    if (bottom !== null) {
        animatePointer(bottom_pointer, "Bottom: " + current_array[bottom]);
    }

    if (middle !== null) {
        animatePointer(middle_pointer, "Middle: " + current_array[middle]);
    }
}

show_step(current_step);
setLabels(current_step);
