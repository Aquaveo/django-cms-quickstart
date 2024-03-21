

var pubsObject = {}
var startLoop = 0
var limit = 25;
let endLoop = 2;
let publicationsData = null
            
let publicationsHtmlElement = document.getElementById('publications-html')
let loadingHtmlElement = document.getElementById('placeholder-publications');
const sleep = (ms = 0) => new Promise(resolve => setTimeout(resolve, ms));

function appendArrayValues(obj1, obj2) {
    let result = {};

    const appendOrAdd = (key, array) => {
        // Ensure result[key] is initialized as an array
        if (!result.hasOwnProperty(key)) {
            result[key] = [];
        }
      
        // Append only unique elements
        array.forEach(element => {
            if (!result[key].includes(element)) {
                result[key].push(element);
            }
        });
    };

    // Append or add values from the first object
    for (const key in obj1) {
        appendOrAdd(key, obj1[key]);
    }

    // Append or add values from the second object
    for (const key in obj2) {
        appendOrAdd(key, obj2[key]);
    }

    return result;
}

const getCSRFToken = () => {
    // Attempt to retrieve the CSRF token from the meta tag
    const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    return token;
}        

const fetchPublications = (start,indexLoop) => {
    // Assuming your Django server is running on localhost:8000
    // Update the URL if your setup is different or if you are using a production server
    requestData['start'] = start
    requestData['limit'] = limit
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // Include the CSRF token in the request headers
        },
        body: JSON.stringify(requestData),
    })
    .then(response => {

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
            return response.json(); // Assuming the response is JSON
        })

    .then(data => {
        console.log(data)
        loadingHtmlElement.classList.remove('hidden')   
        if(!publicationsData){
            publicationsData = data
        }
        else{
            publicationsData = appendArrayValues(publicationsData, data)
        }

        let publicationsHTML = ``

        for (let [key, value] of Object.entries(publicationsData).reverse()) {
            
            //add the year title 
            if (key === '1300'){
                key = 'More Publications'
            }
            
            publicationsHTML += `<h2 class="year-style">${key}</h2>`
            //add the publications
            value.forEach((publication) => {
                publicationsHTML += publication
            })
        }
        publicationsHtmlElement.innerHTML = publicationsHTML;
        
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
        for(var j = 0; j < 3; j++){
            htmlPlaceholders+= `<div class="animated-background publication-background csl-entry" style="height: 70px; margin-bottom:10px !important;"><i></i></div>`   
        }
        htmlPlaceholders+=`</div>`
    }
    placeholdersHtmlElement.innerHTML = htmlPlaceholders;            
}

window.onload = () => {
    create_placeholders();

    let fetchPromises = [];
    for (var i = 0; i < endLoop; i++) {
        // Collect promises returned by fetchPublications
        fetchPromises.push(fetchPublications(startLoop, i));
        startLoop += limit;
    }

    Promise.all(fetchPromises)
        .then(() => {
            loadingHtmlElement.classList.add('hidden');
        })
        .catch(error => {
            console.error("Error with one of the fetch operations:", error);
        });
};