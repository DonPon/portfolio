// personal/static/js/script.js

document.addEventListener('scroll', () => {
    const body = document.body;
    body.classList.add('scrolling');

    // Remove the class after the scroll event ends (after 100ms)
    clearTimeout(body.scrollTimeout);
    body.scrollTimeout = setTimeout(() => {
        body.classList.remove('scrolling');
    }, 100);
});
