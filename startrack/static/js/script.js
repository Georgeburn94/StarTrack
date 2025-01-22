document.addEventListener('DOMContentLoaded', function () {
    const starContainers = document.querySelectorAll('.star-rating');

    starContainers.forEach(container => {
        const number = parseInt(container.getAttribute('data-rating'), 10);

        // Validate the input to ensure it's a non-negative integer
        if (typeof number !== 'number' || number < 0 || !Number.isInteger(number)) {
            console.error('Please provide a non-negative integer.');
            return;
        }

        for (let i = 1; i <= 5; i++) {
            const star = document.createElement('i');
            star.className = 'fa fa-star'; // Font Awesome star icon class
            if (i <= number) {
                star.classList.add('checked');
            }
            container.appendChild(star);
        }
    });

    const addAlbumBtn = document.getElementById("addAlbumBtn");

    addAlbumBtn.addEventListener("click", function () {
        const albumName = document.getElementById("albumName").innerText;
        const albumArtist = document.getElementById("albumArtist").innerText;
        const releaseYear = document.getElementById("releaseYear").innerText;
        const coverImage = document.getElementById("albumCover").src;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        const addAlbumUrl = addAlbumBtn.getAttribute("data-url");

        fetch(addAlbumUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
                name: albumName,
                artist: albumArtist,
                year: releaseYear,
                cover_image: coverImage
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                alert("Album added successfully!");
                // Close the modal
                const modal = bootstrap.Modal.getInstance(document.getElementById("albumDetailsModal"));
                modal.hide();
                // Optionally, reload the page to see the updated list
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch((error) => {
            console.error("Error adding album:", error);
            alert("Something went wrong. Please try again.");
        });
    });

    const fetchDetailsBtn = document.getElementById("fetchDetailsBtn");

    fetchDetailsBtn.addEventListener("click", function () {
        const albumID = document.getElementById("albumID").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
        const fetchUrl = document.getElementById("fetchAlbumForm").dataset.url;

        fetch(fetchUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ album_id: albumID }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error) {
                alert(data.error);
            } else {
                // Populate modal with album details
                document.getElementById("albumCover").src = data.cover_image;
                document.getElementById("albumName").innerText = data.album_name;
                document.getElementById("albumArtist").innerText = data.album_artist;
                document.getElementById("releaseYear").innerText = data.release_year;

                // Show the modal
                new bootstrap.Modal(document.getElementById("albumDetailsModal")).show();
            }
        })
        .catch((error) => {
            console.error("Error fetching album details:", error);
            alert("Something went wrong. Please try again.");
        });
    });
});
