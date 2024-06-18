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


function deleteJournal(journalId) {
    if (confirm("Are you sure you want to delete this journal?")) {
        fetch(`/delete_journal/${journalId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        }).then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("Failed to delete the journal.");
            }
        });
    }
}


function deleteAdmin(adminId) {
    if (confirm("Are you sure you want to delete this admin?")) {
        fetch(`/delete_admin/${adminId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        }).then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert("Failed to delete the admin.");
            }
        }).catch(error => {
            console.error('Error:', error);
            alert("An error occurred while deleting the admin.");
        });
    }
}
