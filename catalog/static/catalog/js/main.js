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

    // Modal de detalle: al hacer clic en una card se muestra la película
    // con su imagen, título y descripción (estilo Netflix).
    const modal = document.getElementById('movie-modal');

    if (modal) {
        const modalHero = document.getElementById('modal-hero');
        const modalTitle = document.getElementById('modal-title');
        const modalDescription = document.getElementById('modal-description');
        const closeButton = modal.querySelector('.modal-close');

        const openModal = (card) => {
            modalTitle.textContent = card.dataset.title || '';
            modalDescription.textContent = card.dataset.description ||
                'Próximamente más detalles de este título.';
            // Copia el fondo de la card (poster subido o gradiente de respaldo)
            modalHero.style.backgroundImage = getComputedStyle(card).backgroundImage;
            modal.hidden = false;
            document.body.style.overflow = 'hidden';
        };

        const closeModal = () => {
            modal.hidden = true;
            document.body.style.overflow = '';
        };

        document.querySelectorAll('.card').forEach((card) => {
            card.addEventListener('click', () => openModal(card));
        });

        closeButton.addEventListener('click', closeModal);

        modal.addEventListener('click', (event) => {
            if (event.target === modal) {
                closeModal();
            }
        });

        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && !modal.hidden) {
                closeModal();
            }
        });
    }
});
