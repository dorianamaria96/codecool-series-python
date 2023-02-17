const apiSearchGenre = '/api/search-actor-by-genre'
const apiSearchName = '/api/search-actor-by-name'
const actorsListUl = document.getElementById('actors')

const selection = document.getElementById('select-genre')
const search = document.getElementById('search-actor')

console.log(selection.value)

getActorFromGenre()

selection.addEventListener('change', (event) => getActorFromGenre(event))
search.addEventListener('input', (event) => getActorFromSearch(event))


function getActorFromGenre() {
    let apiRoute = apiSearchGenre
    console.log('works-select')
    fetch(apiRoute + '?' + new URLSearchParams({
        selectedGenre: document.getElementById('select-genre').value
    }))
        .then(result => result.json())
        .then((actors) => {
            actorsList(actors)
            console.log(selection.value)
        }).catch(error => console.log(error))
}


function getActorFromSearch() {
    let apiRoute = apiSearchName
    console.log('works-search')
    fetch(apiRoute + '?' + new URLSearchParams({
        selectedGenre: document.getElementById('select-genre').value
    }) + '&' + new URLSearchParams({
        searchedActor: document.getElementById('search-actor').value
    }) )
        .then(result => result.json())
        .then((actors) => {
            actorsList(actors)

        }).catch(error => console.log(error))
}

function actorsList(data) {
    actorsListUl.innerHTML = ''
    for (let index = 0; index < data.length; index++) {
        actorsListUl.innerHTML += `
        <li>${data[index].actor}</li>
        `
    }
}


