let currentIndex = 0;

const slides = document.querySelector('.slides');
const slideCount = document.querySelectorAll('.slide').length;
const nextButton = document.getElementById('next');
const prevButton = document.getElementById('prev');

nextButton.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % slideCount;
    updateSlidePosition();
});

prevButton.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + slideCount) % slideCount;
    updateSlidePosition();
});

function updateSlidePosition() {
    slides.style.transform = `translateX(-${currentIndex * 100}%)`;
}
