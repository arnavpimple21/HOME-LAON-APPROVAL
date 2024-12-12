document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const inputs = document.querySelectorAll("input[type='number']");

    form.addEventListener("submit", function(event) {
        let valid = true;
        inputs.forEach(input => {
            if (input.value === "") {
                valid = false;
                input.classList.add("error-input");
            } else {
                input.classList.remove("error-input");
            }
        });

        if (!valid) {
            event.preventDefault();
            alert("Please fill out all fields.");
        }
    });

    inputs.forEach(input => {
        input.addEventListener("input", function() {
            if (input.value !== "") {
                input.classList.remove("error-input");
            }
        });
    });
});
