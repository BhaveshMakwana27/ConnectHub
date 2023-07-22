let addBioBtn = document.getElementById('addBio')

if (addBioBtn != null) {
    addBioBtn.onclick = ()=>{
        if (document.getElementById('bioForm').hidden) {
            document.getElementById('bioForm').hidden = false
        }else{
            document.getElementById('bioForm').hidden = true
        }
    }
}

inputPhoto = document.getElementById('profilePhoto')
if (inputPhoto != null) {
    document.getElementById('profilePhoto').addEventListener('change', function (event) {
        const file = event.target.files[0];
        const imagePreview = document.getElementById('imagePreview');
    
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
        } else {
            imagePreview.innerHTML = '';
        }
    });
}