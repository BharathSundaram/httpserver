document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('uploadForm');
    var progressWrapper = document.getElementById('progressWrapper');
    var progressBar = document.getElementById('progressBar');
    var status = document.getElementById('status');
    
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        var formData = new FormData(form);
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', form.action, true);
        
        xhr.upload.addEventListener('progress', function(e) {
            if (e.lengthComputable) {
                var percentComplete = (e.loaded / e.total) * 100;
                progressBar.value = percentComplete;
                status.textContent = Math.round(percentComplete) + '% uploaded';
            }
        }, false);
        
        xhr.addEventListener('load', function() {
            if (xhr.status === 200) {
                progressBar.value = 100;
                status.textContent = 'Upload complete';
            } else {
                status.textContent = 'Upload failed';
            }
        });
        
        xhr.addEventListener('error', function() {
            status.textContent = 'Upload error';
        });
        
        progressWrapper.style.display = 'block';
        xhr.send(formData);
    });
});
