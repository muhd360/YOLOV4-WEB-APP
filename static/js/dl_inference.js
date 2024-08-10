let globalData = []

// Function to handle pagination click
function handlePaginationClick(pageNumber){

    const startIndex = (pageNumber - 1) * 4;

    const endIndex = startIndex + 4;
    
    const pageData = globalData.slice(startIndex, endIndex);
    
    // populate table 
    populateTable(pageData); // run populate data
}


// Function to create handle pagination links

function createPaginationLinks(totalItems){

    const totalPages = Math.ceil(totalItems / 4);

    const paginationContainer = document.getElementById('pagination');

    paginationContainer.innerHTML = ''; // clear existing links

    for(let i = 1; i <= totalPages; i++){
        const pageLink = document.createElement('a');

        pageLink.href = "#";
        pageLink.textContent = i;

        pageLink.addEventListener('click', (e)=>{

            e.preventDefault();
            handlePaginationClick(i);
        });
        paginationContainer.appendChild(pageLink);
    }
}



async function fetchResultsAndPopulateTable() {

    
    await fetch('/Web_Dev_AI/process-data', {method: 'POST'}) 

        .then(response => {
            if (!response.ok) {
                throw new Error("Network Response was not ok!");
            }
            return response.text();
        })
        .then(dataStr => {
            let data = null;
            try {
                data = JSON.parse(dataStr);
                
                // Check if data is still a string after parsing, which indicates double-encoding
                if (typeof data === 'string') {
                    data = JSON.parse(data);
                }

                // If data is an object (but not an array), maybe it contains the array as a property
                if (typeof data === 'object' && !Array.isArray(data)) {
                    for (let key in data) {
                        if (Array.isArray(data[key])) {
                            data = data[key];
                            break;
                        }
                    }
                }

            } catch (error) {
                console.error('Error parsing the fetched data:', error);
            }
            
            if (Array.isArray(data)) {
                // fetch data globasly 
                globalData = data // store fetch data;
                createPaginationLinks(data.length);
                handlePaginationClick(1);

                console.error('TYPE OUTSIDE POPULATE', typeof(data));
               // populateTable(data);
            } else {
                console.error('Data is not an array after processing:', data);
            }
        })
        .catch(error => {
            console.error('There was an error fetching the results:', error);
        });
}

//stop controller fetch
const controller= new AbortController();

async function fetchRequestHTTPAbort(){

    
    const signal = controller.abort();

    await fetch('/tutorial/process-data', {signal})
    .then(response => {
        if (!response.ok) {
            throw new Error("Network Response was not ok!");
        }
        return response.text();
    }).catch(e => {
        if (e.name === 'AbortError'){
            console.error("error", e.name);
        }
    })
}


function populateTable(data) {
    console.log("INSIDE POPULATE DATA: ", data);
    console.log("TYPE: ", typeof(data));
    let tableBody = document.querySelector("#data-table tbody");

    tableBody.innerHTML = ''; // clear existing page
    
    if (!tableBody) {
        console.error('table body is not found!');
        return;
    }

    

    if (Array.isArray(data)) { // Ensure data is an array

        let existingData = tableBody.querySelectorAll('tr');
    

        data.forEach((item, index) => {

            console.log("Adding row for item:", item);
            console.log("Adding row for INDEX:", index);

            let row;
           /* let row = tableBody.insertRow();*/

           if (existingData && index < existingData.length){

                // insert new row 
                row = existingData[index];

           }else{
              // Insert a new row if there are more items than placeholder rows
                row = tableBody.insertRow();
           }

            let classNameCell = row.insertCell(0);
            let probabilityCell = row.insertCell(1);
            let classIdCell = row.insertCell(2);
            let dateTimeCell = row.insertCell(3);

            classNameCell.textContent = item.class_name || "N/A";
            probabilityCell.textContent = item.probability || "N/A";
            classIdCell.textContent = item.class_id || "N/A";
            dateTimeCell.textContent = item.datetime || "N/A";
        });

    } else {
        console.error('Data is not an array');
    }
}


//event listeniner for do inference

document.getElementById('doInference').addEventListener('click', function(){

    fetchResultsAndPopulateTable();
});



// event listener for stop inference

document.getElementById('stopInference').addEventListener('click', function(){

    fetchRequestHTTPAbort();

});