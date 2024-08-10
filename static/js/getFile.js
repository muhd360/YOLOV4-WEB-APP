
function displayImage(imageFilename) {
        const imageUrl = window.location.origin + 'static/uploads/' + imageFilename;
        document.getElementById('image').src = imageUrl;
}

