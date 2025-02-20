document.addEventListener('DOMContentLoaded', function() {
    const fetchForm = document.getElementById('fetchAlbumForm');
    const fetchBtn = document.getElementById('fetchDetailsBtn');

    if (fetchBtn) {
        fetchBtn.addEventListener('click', function() {
            const albumQuery = document.getElementById('albumID').value;
            const url = fetchForm.dataset.url;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ 'album_query': albumQuery })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    // Update modal elements with the new data structure
                    document.getElementById('albumCover').src = data.cover_image;
                    document.getElementById('albumName').textContent = data.name;
                    document.getElementById('albumArtist').textContent = data.artist;
                    document.getElementById('releaseYear').textContent = data.year;
                    
                    // Store the formatted album data for later use
                    const modal = document.getElementById('albumDetailsModal');
                    modal.dataset.albumData = JSON.stringify({
                        name: data.name,
                        artist: data.artist,
                        year: data.year,
                        cover_image: data.cover_image,
                        tracks: data.tracks
                    });
                    
                    // Show the modal
                    new bootstrap.Modal(modal).show();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to fetch album details');
            });
        });
    }

    // Handle the Add Album button click
    const addAlbumBtn = document.getElementById('addAlbumBtn');
    if (addAlbumBtn) {
        addAlbumBtn.addEventListener('click', function() {
            const modal = document.getElementById('albumDetailsModal');
            const albumData = JSON.parse(modal.dataset.albumData);
            const url = addAlbumBtn.dataset.url;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(albumData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Album added successfully!');
                    location.reload();
                } else {
                    alert('Failed to add album: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to add album');
            });
        });
    }
});