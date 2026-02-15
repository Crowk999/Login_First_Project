const links = document.querySelectorAll("a");

links.forEach(link => {
    link.addEventListener("click", (e) => {
        e.preventDefault();

    const form = document.querySelector("form");
    form.classList.add("flip");

    setTimeout(() => {
            window.location.href = link.href;
        }, 800);
    });

}); 