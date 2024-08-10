function displayImage(imageFilename) {

  const imageUrl = window.location.origin + 'static/uploads/' + imageFilename;
  document.getElementById('image').src = imageUrl;
}

function animate_title(id){
	let element = document.getElementById(id);
  let text = element.innerHTML;
  setInterval(() => {
  	text = text[text.length - 1] + text.substring(0, text.length - 1 );
    element.innerHTML = text;
  }, 500);

}


function showImageName() {
  var name = document.getElementById('myfile');
  var filename = name.value.split(/(\\|\/)/g).pop(); // extract file name from path
  document.getElementById('getName').innerHTML = "Image Chosen: " + filename;
}


async function populateSideBar(){

    console.log("Populate Side Initialzied");


    const varSideBar = document.getElementById('sidebar');
    const ul = varSideBar.querySelector('ul');
    ul.innerHTML = '';

    // Create and append the home icon list item
    const homeLi = document.createElement('li');
    homeLi.className = 'nav-item';

    const homeLink = document.createElement('a');
    homeLink.className = 'nav-link';
    homeLink.href = '#';  // Change this to your home page URL
    homeLink.innerHTML = '<i class="fas fa-home"></i> Home';  // FontAwesome home icon

  try{

    const response = await fetch("/Web_Dev_AI/last-uploaded");  

    if (!response.ok){
      console.log("Response Fetch Failed");
    }
    else{
      const files = await response.json();
      console.log("Files", files);

      files.forEach(file => {
        const li = document.createElement('li');
        li.className = 'nav-item';

        const a = document.createElement('a');

        a.className = 'nav-link';
        a.href = '#';
        a.textContent = file;

        li.appendChild(a);
        ul.appendChild(li);
        
      });
    }
  }
  catch(error){
    console.log("Error", error);
  }

}
populateSideBar();




