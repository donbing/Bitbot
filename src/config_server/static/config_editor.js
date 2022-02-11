
// 🔗 open element href in a modal dialog
function editFile(element)
{
    let dialog = element.nextElementSibling;
    fetch(element.href)
        .then(response => response.text())
        .then(html => {
            dialog.innerHTML = html;
            dialog.showModal();
            AutoComplete();
        })
        .catch(function (err) {
            console.warn('Something went wrong.', err);
        });

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


(() => {
    fetch('/logs')
      .then(response => {
        const elem = document.getElementById('log_output');
        const reader = response.body.getReader();
        const readStream = ({ done,value }) => {
          if (done) {
            return;
          }
          let chunk = String.fromCharCode.apply(null, value);
          elem.textContent += chunk + '\n';
          return reader.read().then(readStream);
        };
        reader.read().then(readStream);
      });
})();