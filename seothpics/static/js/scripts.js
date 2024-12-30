document.addEventListener('DOMContentLoaded', function() {
    // Function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Show alert message
    function showAlert(message, type) {
        const alertContainer = document.getElementById('alert-container');
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.role = 'alert';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        alertContainer.appendChild(alert);

        // Automatically remove the alert after 3 seconds
        setTimeout(() => {
            $(alert).alert('close');
        }, 3000);
    }

    // Download image script
    const downloadLinks = document.querySelectorAll('.download');
    downloadLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const imageUrl = this.href;
            const imageId = this.getAttribute('data-image-id');

            // Start the download
            const anchor = document.createElement('a');
            anchor.href = imageUrl;
            anchor.setAttribute('download', '');
            document.body.appendChild(anchor);
            anchor.click();
            document.body.removeChild(anchor);

            // Make an AJAX call to update the download count
            fetch(`/download_image/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ image_id: imageId })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    // Like image script
    const likeLinks = document.querySelectorAll('.like-icon');
    likeLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const imageId = this.getAttribute('data-image-id');

            // Make an AJAX call to update the like count
            fetch(`/like_image/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ image_id: imageId })
            })
            .then(response => response.json())
            .then(data => {
                showAlert('You liked this image!', 'success');
                // Optionally update the like icon or like count here
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });

    // Search image script
    const searchForm = document.querySelector('form');
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const searchInput = document.querySelector('.search-input').value;

        // Make an AJAX call to search images
        fetch(`/search_image/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ search_term: searchInput })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const galleryContainer = document.querySelector('.gallery-container');
                galleryContainer.innerHTML = ''; // Clear current images

                // Display search results
                data.images.forEach(image => {
                    const galleryItem = document.createElement('div');
                    galleryItem.className = 'gallery-item';
                    galleryItem.innerHTML = `
                        <img src="${image.image_file}" alt="${image.name}" loading="lazy" class="img-fluid">
                        <div class="icons">
                            <a href="#" class="top-right like-icon" data-image-id="${image.id}" id="like-${image.id}">
                                <i class="fas fa-heart"></i>
                            </a>
                            <a href="#" class="top-right"><i class="fas fa-share"></i></a>
                            <a href="${image.image_file}" download class="download" data-image-id="${image.id}" id="download-${image.id}">
                                <i class="fas fa-download"></i>
                            </a>
                        </div>
                    `;
                    galleryContainer.appendChild(galleryItem);
                });

                // Reinitialize like and download listeners
                initializeLikeAndDownloadListeners();
            } else {
                showAlert('No images found. Please try a different search term.', 'warning');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function initializeLikeAndDownloadListeners() {
        // Reinitialize download listeners
        const downloadLinks = document.querySelectorAll('.download');
        downloadLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const imageUrl = this.href;
                const imageId = this.getAttribute('data-image-id');

                // Start the download
                const anchor = document.createElement('a');
                anchor.href = imageUrl;
                anchor.setAttribute('download', '');
                document.body.appendChild(anchor);
                anchor.click();
                document.body.removeChild(anchor);

                // Make an AJAX call to update the download count
                fetch(`/download_image/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ image_id: imageId })
                })
                .then(response => response.json())
                .then(data => {
                    console.log(data.message);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        });

        // Reinitialize like listeners
        const likeLinks = document.querySelectorAll('.like-icon');
        likeLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const imageId = this.getAttribute('data-image-id');

                // Make an AJAX call to update the like count
                fetch(`/like_image/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ image_id: imageId })
                })
                .then(response => response.json())
                .then(data => {
                    showAlert('You liked this image!', 'success');
                    // Optionally update the like icon or like count here
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        });
    }
});
