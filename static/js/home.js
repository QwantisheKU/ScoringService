
let searchForm = document.getElementById('searchForm')
let pageItems = document.getElementsByClassName('page-link')
    
if(searchForm) {
    for(let i=0; pageItems.length > i; i++) {
        pageItems[i].addEventListener('click', function (e) {
            e.preventDefault()

            let page = this.dataset.page
              
            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`
            searchForm.submit()
        })
    }
}
