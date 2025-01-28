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
});

document.addEventListener('DOMContentLoaded', function() {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function(toastEl) {
        return new bootstrap.Toast(toastEl)
    })
    toastList.forEach(toast => toast.show())
});