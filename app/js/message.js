const scriptURL = 'https://script.google.com/macros/s/AKfycbyY5mRlacmnunftg-DfchdoH8JIZuxQuG5RvA2wcH8lmSmTmL-4_PVV-r9w1aq4dQXk/exec'
const form = document.forms['product']
form.addEventListener('submit', e => {
  e.preventDefault()
  fetch(scriptURL, { method: 'POST', body: new FormData(form) })
    .then(response => alert("Thank You! We Got Your Message Successfully."))
    .then(() => { window.location.reload(); })
    .catch(error => console.error('Error!', error.message))
})