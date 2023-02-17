const detailedInformation = document.getElementById('selected-show')
const apiRoute = '/api/shows-with-more-than-5-genres'
const dropdown = document.getElementById('select-show')

dropdown.addEventListener('change', (event) => getDetailedInformation(apiRoute))


function getDetailedInformation (route = apiRoute ) {
    fetch(route + '?' + new URLSearchParams({
        selectedShow: dropdown.value
    }))
        .then(response => response.json())
        .then(details => {
            detailedInformation.innerHTML = `
            <li>${details[0].production_year}</li>
            <li>${details[0].number_of_seasons}</li>`
        })
}
