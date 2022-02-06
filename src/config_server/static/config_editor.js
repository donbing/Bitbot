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
document.querySelectorAll('dialog').forEach(item => 
    item.addEventListener('click', event => {
        const rect = event.currentTarget.getBoundingClientRect();
        if (event.clientY < rect.top || event.clientY > rect.bottom ||
            event.clientX < rect.left || event.clientX > rect.right) {
                event.currentTarget.close();
        }
    })
);
