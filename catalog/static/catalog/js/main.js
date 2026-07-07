document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.getElementById('navbar');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 60) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    document.querySelectorAll('.row-track-wrapper').forEach((wrapper) => {
        const track = wrapper.querySelector('.row-track');
        const leftArrow = wrapper.querySelector('.row-arrow-left');
        const rightArrow = wrapper.querySelector('.row-arrow-right');
        const scrollAmount = 600;

        leftArrow.addEventListener('click', () => {
            track.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
        });

        rightArrow.addEventListener('click', () => {
            track.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        });
    });

    document.querySelectorAll('.card').forEach((card) => {
        card.addEventListener('click', () => {
            const title = card.querySelector('.card-title').textContent;
            alert(`Reproduciendo: ${title}`);
        });
    });
});
