

const getCSRFToken = () => {
    // Attempt to retrieve the CSRF token from the meta tag
    const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    return token;
}        

const fetchHydroShareResources = () => {
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
            document.getElementById('placeholder-hydroshare-resources').classList.add('hidden'); 
            document.getElementById('hydroshare-resources-list-plugin').classList.remove('hidden'); 

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
            return response.json(); // Assuming the response is JSON
        })
        .then(data => {                
            let resourcesHTML = ``
            data['resources'].forEach(resource => {
                resourcesHTML += `
                <div class="hydroshare_resource card mb-3 w-100 card-height" >
                <div class="row g-0">
                    <div class="col-12 col-sm-6 col-md-4 col-lg-4 d-flex justify-content-center  align-items-center" >`
                if (resource.web_site_url){
                    resourcesHTML += `
                    <header class="course-image">
                        <div class="cover-image">
                            <a href="${resource.web_site_url}">
                                <img src="${resource.image}" class="img-tile img-fluid rounded-start" alt="..."  style="width:200px; height:200px;" >
                            </a> 
                            <div class="learn-more" aria-hidden="true">`
                            if (resource.resource_type == 'ToolResource'){
                                resourcesHTML += `<a href="${resource.web_site_url}">Open Application</a>`
                            }
                            else{
                                resourcesHTML += `<a href="${resource.web_site_url}">Open Resource</a>`
                            }
                            resourcesHTML += `</div></div></header></div>`
                
                }
                else{
                    resourcesHTML += `
                    <a href='javascript:void(0)' class='portfolio-link'>
                        <img src="${resource.image}" class="img-tile img-fluid rounded-start h-100" alt="..." style="width:200px; height:200px;">
                    </a></div>`
                }
                resourcesHTML += `
                    <div class="col-12 col-sm-6 col-md-8 col-lg-8 border-light">
                        <div class="card-body h-100">
                            <div class="d-flex align-items-baseline gap-2 justify-content-center justify-content-lg-start justify-content-md-start">
                            
                                <h6 class="card-title card-h5">${resource.title}</h6>`

                resourcesHTML += `<div style="width:fit-content;">`
                resourcesHTML +=`<p class="card-text my-2 fs-6 lh-1.5 fw-light d-flex flex-row justify-content-between w-100 gap-3 rounded p-1"  style="max-width:300px;">`
                if(resource.github_url){
                    resourcesHTML +=`<a href="${resource.github_url}" target="_blank" class="text-decoration-none text-secondary" title="Source Code"> <i class="bi bi-github"></i></a>`
                }
                if(resource.web_site_url){
                    resourcesHTML +=`<a href="${resource.web_site_url}" target="_blank" class="text-decoration-none text-secondary" title="Web page"> <i class="bi bi-arrow-up-right-square"></i> </a>`
                }
                if(resource.documentation_url){
                    resourcesHTML +=`<a href="${resource.documentation_url}" target="_blank" class="text-decoration-none text-secondary" title="Documentation"> <i class="bi bi-journals"></i> </a>`
                }
                // resourcesHTML +=`<a href="${resource.resource_url}" target="_blank" class="text-decoration-none text-secondary" style="font-size: 0.80rem !important;" title="Open HydroShare Resource"> <span class="badge text-bg-secondary">HydroShare</span></a>`
                resourcesHTML +=`</p></div></div>`

                
                resourcesHTML +=`<p class="card-subtitle mb-2 text-muted d-flex justify-content-center justify-content-lg-start justify-content-md-start justify-content-xl-start"><a href="${resource.resource_url}" target="_blank" class="text-decoration-none text-secondary" style="font-size: 0.80rem !important;" title="Open HydroShare Resource"> <span class="badge text-bg-secondary">View on HydroShare</span></a></p>`

                resourcesHTML +=`<div class="d-flex flex-column justify-content-lg-start justify-content-md-start text-center text-lg-start text-md-start h-100">
                                <p class="name w-100 mb-3 overflow-auto">
                                    ${resource.abstract}
                                </p>
                </div>`
                resourcesHTML += `</div></div></div></div>`

            });

            document.getElementById('hydroshare-resources-list-plugin').innerHTML = resourcesHTML;

        // For example, you could iterate over the data and append it to an element in your HTML
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }
    
const create_placeholders = () => {
    let placeholdersHtmlElement = document.getElementById('placeholder-hydroshare-resources');
    let htmlPlaceholders = '';
    for(var i = 0; i < 10; i++){
        htmlPlaceholders+=`
        <div class="card mb-3 w-100 card-height" >
        <div class="row g-0">
            <div class="animated-background descriptions-background col-12 col-sm-6 col-md-4 col-lg-4 d-flex justify-content-center justify-content-md-end justify-content-lg-end align-items-center align-items-lg-center align-items-md-center" >

                <header class="course-image">
                    <div class="cover-image">

                    
                    </div>
                </header>

            </div>
            <div class="col-12 col-sm-6 col-md-8 col-lg-8 border-light">
                <div class="card-body" style="background:white;">
                    <div class="d-flex align-items-baseline gap-2 justify-content-center justify-content-lg-start justify-content-md-start">
                        <h5 class="card-title card-h5 animated-background titles-loading-background" style="width: 50%; height:20px;" ></h5>
                    </div>
  
                    <p class="animated-background titles-loading-background card-subtitle mb-2 text-muted fst-italic" style="height:20px; width:25%;"></p>

                    <div class="animated-background descriptions-background d-flex flex-column justify-content-center justify-content-lg-start justify-content-md-start text-center text-lg-start text-md-start">
                        <p class="name w-100 mb-3 overflow-auto">
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
            
        `
    }
    placeholdersHtmlElement.innerHTML = htmlPlaceholders;            
}

create_placeholders();
fetchHydroShareResources();
