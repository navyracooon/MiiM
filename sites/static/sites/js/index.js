function message_copied() {
    const copied = document.getElementById('copied-message')

    copied.classList.add('fadeout')
    setTimeout(
        function() {
            copied.classList.remove('fadeout')
        },
        2500
    );
}