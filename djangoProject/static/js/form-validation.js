document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("create-post-form");

    form.addEventListener("submit", function (event) {
        let isValid = true;

        if (CKEDITOR.instances.body) {
            CKEDITOR.instances.body.updateElement();
        }

        const title = document.getElementById("title");
        if (!title.value.trim()) {
            title.classList.add("is-invalid");
            isValid = false;
        } else {
            title.classList.remove("is-invalid");
        }

        const body = document.getElementById("body");
        if (!body.value.trim()) {
            body.classList.add("is-invalid");
            isValid = false;
        } else {
            body.classList.remove("is-invalid");
        }

        if (!isValid) {
            event.preventDefault();
        }
    });
});
