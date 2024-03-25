// if local publications is bigger than one, then used as an start index to fetch new publications.


// var startLoop = totalLocalPublications > 1 ? totalLocalPublications : 0
// var startLoop = 0
let LIMIT = 10;
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

const inititialFetchPublications = (start) => {
    // Update the URL if your setup is different or if you are using a production server
    let newRequestData =  requestData
    newRequestData['start'] = start
    newRequestData['limit'] = LIMIT
    // newRequestData['isRemote'] = total_publications > totalLocalPublications
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




const fetchPublications = (start) => {
    // Update the URL if your setup is different or if you are using a production server
    let newRequestData =  requestData
    newRequestData['start'] = start
    newRequestData['limit'] = LIMIT
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
console.log(total_publications)


const fetchAndProcessPublicationsSequentially = async () => {

    // Start the loop based on the total number of local publications
    let startLoop = totalLocalPublications > 1 ? totalLocalPublications : 0;

    let differencePublications = total_publications - totalLocalPublications;

    // if the difference is negative, it means that publications were deleted, so start with index 0
    startLoop = differencePublications < 0 ? 0 : startLoop;

    console.log("Difference in publications:", differencePublications);
    
    if (totalLocalPublications == 0){
        let iterations = differencePublications > 0 ? Math.ceil(differencePublications / LIMIT) : Math.ceil(total_publications / LIMIT);

        console.log("Number of iterations:", iterations);

        
        for (let i = 0; i < iterations; i++) {
            try {
                await inititialFetchPublications(startLoop);
                startLoop += LIMIT;
            } catch (error) {
                console.error("Error with one of the fetch operations:", error);
                // Optionally break or continue based on your error handling preferences
                break;
            }
        }
    }
    else{
        LIMIT = Math.abs(differencePublications) //only search for the most recent items added to the library
        await fetchPublications(startLoop);
    }


    // // if new publications were added or deleted, fetch them
    // if (differencePublications > 0) {
    //     // Adjust the loop based on whether you need to add new ones or refetch all
    //     let iterations = differencePublications > 0 ? Math.ceil(differencePublications / LIMIT) : Math.ceil(total_publications / LIMIT);

    //     console.log("Number of iterations:", iterations);

        
    //     for (let i = 0; i < iterations; i++) {
    //         try {
    //             await fetchPublications(startLoop);
    //             startLoop += LIMIT;
    //         } catch (error) {
    //             console.error("Error with one of the fetch operations:", error);
    //             // Optionally break or continue based on your error handling preferences
    //             break;
    //         }
    //     }
    // } 
    // if(differencePublications < 0){
    //     // let iterations = Math.ceil(total_publications / LIMIT);

    //     LIMIT = Math.abs(differencePublications) //only search for the most recent items added to the library
    //     await fetchPublications(startLoop);

    // }
    // if(differencePublications==0) {
    //     console.log("No changes, retrieving from database or using cached data");
    //     await fetchPublications(startLoop);
    // }

    // Hide the loading HTML element once all operations are complete
    loadingHtmlElement.classList.add('hidden');
};

// Ensure to call your function in an async context
fetchAndProcessPublicationsSequentially().then(() => {
    console.log("All publications processed.");
}).catch(error => {
    console.error("An error occurred during the publication fetching process:", error);
});



// //second iteration
// if(total_publications > 0){
//     let fetchPromises = [];
//     let differencePublications = total_publications - totalLocalPublications;

//     //making batch requests
//     console.log("difference in publications",differencePublications)
    
//     // publications were added to the remote library, in this case just add the new ones
//     if (differencePublications > 0){
//         console.log("new applications added")
//         for (var i = 0; i < Math.ceil(differencePublications/LIMIT); i++) {
//             // Collect promises returned by fetchPublications
//                 fetchPromises.push(fetchPublications(startLoop));
//                 startLoop += LIMIT;
//         }
//     }
//     // publications were deleted in the library, in this case just add all of them again
//     else if(differencePublications < 0){
//         console.log("applications deleted")
//         startLoop = 0 //reset the startLoop, we are going to fetch all the publications again
//         for (var i = 0; i < Math.ceil(total_publications/LIMIT); i++) {
//             // Collect promises returned by fetchPublications
//                 fetchPromises.push(fetchPublications(startLoop));
//                 startLoop += LIMIT;
//         }
//     } 
//     // retrieving from database if they are the same.
//     else{
//         console.log("no changes, retrieving from database")
//         fetchPromises.push(fetchPublications(startLoop));
//     }

//     Promise.all(fetchPromises)
//         .then(() => {
//             loadingHtmlElement.classList.add('hidden');
//         })
//         .catch(error => {
//             console.error("Error with one of the fetch operations:", error);
//         });
    
// }









//first edit 

// if(total_publications > 0){
//     let fetchPromises = [];
//     let differencePublications = total_publications - totalLocalPublications;

//     for (var i = 0; i < Math.ceil(total_publications/LIMIT); i++) {
//         // Collect promises returned by fetchPublications
//         if(total_publications > startLoop){
//             fetchPromises.push(fetchPublications(startLoop));
//             startLoop += LIMIT;
//         }
//     }
    
//     Promise.all(fetchPromises)
//         .then(() => {
//             loadingHtmlElement.classList.add('hidden');
//         })
//         .catch(error => {
//             console.error("Error with one of the fetch operations:", error);
//         });
    
// }