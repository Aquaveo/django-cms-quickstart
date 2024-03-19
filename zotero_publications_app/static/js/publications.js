

const getCSRFToken = () => {
    // Attempt to retrieve the CSRF token from the meta tag
    const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    return token;
}        

const fetchPublications = () => {
    // Assuming your Django server is running on localhost:8000
    // Update the URL if your setup is different or if you are using a production server
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // Include the CSRF token in the request headers
        },
        body: JSON.stringify(requestData),
    })
        .then(response => {
            document.getElementById('placeholder-publications').classList.add('hidden'); // Hide spinner
            document.getElementById('publications-html').classList.remove('hidden'); // Show content
            
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
            return response.json(); // Assuming the response is JSON
        })
        .then(data => {
            let publicationsHTML = ``
            for (const [key, value] of Object.entries(data)) {
                //add the year title 
                publicationsHTML += `<h2 class="year-style">${key}</h2>`
                //add the publications
                value.forEach((publication) => {
                    publicationsHTML += publication
                })
            }
            document.getElementById('publications-html').innerHTML = publicationsHTML;

        // For example, you could iterate over the data and append it to an element in your HTML
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }
const create_placeholders = () => {
    let placeholdersHtmlElement = document.getElementById('placeholder-publications');
    let htmlPlaceholders = '';
    for(var i = 0; i < 10; i++){
        htmlPlaceholders+=`<h2 class="animated-background year-loading-background year-style" style="height:50px;"></h2><div class="csl-bib-body" style="line-height: 2; padding-left: 1em; text-indent:-1em;">`
        for(var j = 0; j < 5; j++){
            htmlPlaceholders+= `<div class="animated-background publication-background csl-entry" style="height: 70px; margin-bottom:10px !important;"><i></i></div>`   
        }
        htmlPlaceholders+=`</div>`
    }
    placeholdersHtmlElement.innerHTML = htmlPlaceholders;            
}

create_placeholders();
fetchPublications();
