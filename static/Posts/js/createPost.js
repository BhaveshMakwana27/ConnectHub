document.getElementById('postImages').addEventListener('change', function(e) {
    var files = e.target.files; // Get the selected files

    // Clear previous previews
    document.getElementById('previewImage').innerHTML = '';

    // Loop through the selected files and create image previews
    for (var i = 0; i < files.length; i++) {
      var file = files[i];
      if (file.type.startsWith('image/')) {
        var reader = new FileReader();
        reader.onload = function(event) {
          var img = document.createElement('img');
          img.src = event.target.result;
          document.getElementById('previewImage').appendChild(img);
        };
        reader.readAsDataURL(file);
      }
    }
  });