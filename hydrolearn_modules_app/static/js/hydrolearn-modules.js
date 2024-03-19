

const getCSRFToken = () => {
    // Attempt to retrieve the CSRF token from the meta tag
    const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    return token;
}        

const fetchLearningModules = () => {
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
            console.log(response);
            document.getElementById('placeholder-hydrolearn-modules').classList.add('hidden'); 
            document.getElementById('hydrolearn-modules-plugin').classList.remove('hidden'); 

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
            return response.json(); // Assuming the response is JSON
        })
        .then(data => {
            console.log(data);
                
            let modulesHTML = ``
            data['modules'].forEach(module => {
                modulesHTML += `
                <div class="hydrolearn_module card mb-3 w-100 card-height" >
                <div class="row g-0">
                    <div class="col-12 col-sm-6 col-md-4 col-lg-4 d-flex justify-content-center justify-content-md-end justify-content-lg-end align-items-center align-items-lg-center align-items-md-center" >`
                if (module.course_url){
                    modulesHTML += `
                    <header class="course-image">
                        <div class="cover-image">
                            <a href="${module.course_url}">
                                <img src="${module.course_image_url}" class="img-tile img-fluid rounded-start" alt="..." >
                            </a> 
                            <div class="learn-more" aria-hidden="true">
                                <a href="${module.course_url}">OPEN MODULE</a>
                            </div>
                        
                        </div>
                    </header>
                </div>`
                
                }
                else{
                    modulesHTML += `
                    <header class="course-image">
                        <div class="cover-image">
                            <a href='javascript:void(0)' class='portfolio-link'>
                                <img src="${module.course_image_url}" class="img-tile img-fluid rounded-start h-100" alt="..." >
                            </a>
                            <div class="learn-more" aria-hidden="true">
                                <a href="https://edx.hydrolearn.org/courses">OPEN MODULE</a>
                            </div>
                            
                        </div>
                    </header>
                    </div>`
                }
                modulesHTML += `
                    <div class="col-12 col-sm-6 col-md-8 col-lg-8 border-light">
                        <div class="card-body">
                            <div class="d-flex align-items-baseline gap-2 justify-content-center justify-content-lg-start justify-content-md-start">
                                <h5 class="card-title card-h5">${module.course_title}</h5>
                            </div>
                                <div class="row g-0">
                                    <div class="col col-md-6 col-lg-6 col-xl-6 text-start">
                                        <p class="card-subtitle mb-2 text-muted" style="font-size:12px;">`
                if ( module.course_organization){
                    modulesHTML +=`<span class="text-muted">${module.course_organization}</span>`

                }
                modulesHTML += `</p></div>`               
                modulesHTML += `
                                <div class="col col-md-6 col-lg-6 col-xl-6 text-end">
                                        <p class="card-subtitle mb-2 text-muted" style="font-size:12px">`
                if(module.course_code){
                    modulesHTML += `<span class="text-muted">${module.course_code }</span>`
                }
                modulesHTML += `</p></div></div>`

                if (module.course_weekly_effort){
                    modulesHTML +=`<p class="card-subtitle mb-2 text-muted fst-italic" style="font-size:12px;">Effort: ${module.course_weekly_effort}</p>`
                }
                modulesHTML +=`
                <div class="d-flex flex-column justify-content-center justify-content-lg-start justify-content-md-start text-center text-lg-start text-md-start">
                                <p class="name w-100 mb-3 overflow-auto">
                                    ${module.course_description_content}
                                </p>
                </div>`
                modulesHTML += `</div></div></div></div>`

            });

            document.getElementById('hydrolearn-modules-plugin').innerHTML = modulesHTML;

        // For example, you could iterate over the data and append it to an element in your HTML
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    }
const create_placeholders = () => {
    let placeholdersHtmlElement = document.getElementById('placeholder-hydrolearn-modules');
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
fetchLearningModules();
