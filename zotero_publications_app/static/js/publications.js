let publicationsData = null
            
let publicationsHtmlElement = document.getElementById('publications-html')
let loadingHtmlElement = document.getElementById('placeholder-publications');


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

const parseDataResponse = (data) =>{
    // console.log(data)
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
}

const inititialFetchPublications = () => {
    // Update the URL if your setup is different or if you are using a production server
    let newRequestData =  requestData

    newRequestData['totalLocalPublications'] = totalLocalPublications
    newRequestData['totalRemotePublications'] = total_publications
    newRequestData['instanceID'] = instanceID

    return fetch(init_pubs_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // Include the CSRF token in the request headers
        },
        body: JSON.stringify(newRequestData),
    })
    .then(response => {

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
            return response.json(); // Assuming the response is JSON
        })

    .then(data => {
        parseDataResponse(data)

    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}




const fetchPublications = () => {
    // Update the URL if your setup is different or if you are using a production server
    let newRequestData =  requestData

    // newRequestData['isRemote'] = total_publications > totalLocalPublications
    newRequestData['totalLocalPublications'] = totalLocalPublications
    newRequestData['totalRemotePublications'] = total_publications

    newRequestData['instanceID'] = instanceID
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // Include the CSRF token in the request headers
        },
        body: JSON.stringify(newRequestData),
    })
    .then(response => {

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
            return response.json(); // Assuming the response is JSON
        })

    .then(data => {
        // console.log(data)
        parseDataResponse(data);
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




const get_items_counts = async () => {
    // function to get total count of items in remote library/collection
    try {
        let requestDataAdded = requestData;
        requestDataAdded['instanceID'] = instanceID
        const response = await fetch(url_item_count, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken(), // Include the CSRF token in the request headers
            },
            body: JSON.stringify(requestData),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json(); // Assuming the response is JSON
        return data['number_items'];
    } catch (error) {
        console.error('Error:', error);
    }
};


// create placeholders for the loading
create_placeholders();



// get the total number of publications in the library
let total_publications = await get_items_counts();

const fetchAndProcessPublicationsSequentially = async () => {
    
    if (totalLocalPublications == 0){
        await inititialFetchPublications();
 
    }
    else{
        await fetchPublications();
    }

    // Hide the loading HTML element once all operations are complete
    loadingHtmlElement.classList.add('hidden');
};

// Ensure to call your function in an async context
fetchAndProcessPublicationsSequentially().then(() => {
    console.log("All publications processed.");
}).catch(error => {
    console.error("An error occurred during the publication fetching process:", error);
});

