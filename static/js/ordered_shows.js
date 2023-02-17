const apiOrderShowsRoute = '/api/ordered-shows'
const tableBodyContent = document.getElementById('ordered-shows')
const changeOrderBtn =document.getElementById('change-order')

let sortState = 'ASC'

getOrderedShow(apiOrderShowsRoute);
changeOrderBtn.addEventListener("click", () => getOrderedShow(apiOrderShowsRoute))

function getOrderedShow(route = apiOrderShowsRoute) {
    fetch(route + '?' + new URLSearchParams({
    sortState: sortState
    }))
        .then(result => result.json())
        .then((shows) => {
            if (sortState === 'ASC') {
                sortState = 'DESC'
            } else {
                sortState = 'ASC'
            }
            console.log(shows)
            createContent(shows);
        }).catch(error => console.log(error))
}

function createContent(data) {
    tableBodyContent.innerHTML =''
    for (let index = 0; index < data.length; index++) {
        let star = '☆'
        let stars = star.repeat(parseInt(data[index].rating))
        tableBodyContent.innerHTML += `
        <tr>
            <td>${data[index].title}</td>
            <td>${stars}</td>
        </tr>`
    }
}


