const actorsApi = '/api/actors2'

const detailedInformation = document.getElementById('actors-work')
const ulActors = document.querySelectorAll('.list-shows')


ulActors.forEach((ulActor) => {
  ulActor.addEventListener('click', () => {
        actorShows(actorsApi, ulActor.id);
      console.log(ulActor.id)
  });
});


function actorShows(url, actors_id) {
    fetch(url +'?'+ new URLSearchParams({
        actorsWork: actors_id
    }))
        .then(response => response.json())
        .then(shows => {
            let detailedInformation = document.getElementById('actor-' + actors_id)
            console.log('WORKS')
            console.log(shows)
            detailedInformation.innerHTML= ''
            for (let index = 0; index < shows.length; index++) {
                console.log(shows[index].title)
                detailedInformation.innerHTML += `
                <li>${shows[index].title}</li>`
            }
        })

}

