document.getElementById('profilePhoto').addEventListener('change', function (event) {
    const file = event.target.files[0];
    const imagePreview = document.getElementById('previewImage');

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.classList.add('img-thumbnail');
            imagePreview.innerHTML = '';
            imagePreview.appendChild(img);
        }
        reader.readAsDataURL(file);
        document.getElementById('default-image').remove()
    } else {
        imagePreview.innerHTML = '';
    }
});