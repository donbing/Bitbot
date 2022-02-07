
// 🔗 open element href in a modal dialog
function editFile(element)
{
    let dialog = element.nextElementSibling;
    var request = new XMLHttpRequest();
    request.open("GET", element.href, true);
    request.send(null);
    request.onreadystatechange = function() {
        if (request.readyState == 4)
        {
            dialog.innerHTML = request.responseText;
            dialog.showModal();
        };
    };
    return false;
}

// ❌ close dialog on click outside
document.querySelectorAll('dialog').forEach(dialog => {
    
    // register with polyfill for FF/iOS supporrt
    dialogPolyfill.registerDialog(dialog)

    dialog.addEventListener('click', click => {
        const rect = dialog.getBoundingClientRect();
        if (click.clientY < rect.top || click.clientY > rect.bottom ||
            click.clientX < rect.left || click.clientX > rect.right) {
                dialog.close();
        }
    });

    dialog.addEventListener('submit', submit => {
        submit.preventDefault();

        var form = dialog.querySelector('form');
        var xhr = new XMLHttpRequest();
        xhr.open("POST", form.action);
        xhr.send(new FormData(form));
        xhr.onreadystatechange = () => {
            if (xhr.readyState == 4)
                dialog.close();
        };
    });
});