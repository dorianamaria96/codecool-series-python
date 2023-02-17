console.log('shows by letter')

const urlShowsByLetter = '/api/shows-by-letter'
const tableShowData = document.getElementById('show-data')
const letterButtons = document.querySelectorAll('.letter-button')


class (button1('a'), button2('b'), button3('c'))



letterButtons.forEach(letterButton => {
    letterButton.addEventListener('click', () => displayShowsByLetter(letterButton.id, urlShowsByLetter))
})

function displayShowsByLetter(shit, fuck) {
    fetch(fuck + '?' + new URLSearchParams({
        letter: shit
    }))
        .then(response => response.json())
        .then(shows => {
            console.log('hello I am fetching successfully')
        })
}
