const stars = document.querySelectorAll('.star');
  
stars.forEach(star => {
  star.addEventListener('click', function() {
    const value = this.getAttribute('data-value');
    const starsContainer = this.parentElement;
    const stars = Array.from(starsContainer.children);

    stars.forEach(star => {
      if (star.getAttribute('data-value') <= value) {
        star.classList.add('checked');
      } else {
        star.classList.remove('checked');
      }
    });

    document.getElementById('rating').value = value;
    starsContainer.setAttribute('data-rating', value);
  });
});

document.getElementById('feedbackForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const formData = new FormData(this);
  const feedbackData = Object.fromEntries(formData.entries());

  console.log('Submitted feedback:', feedbackData);
});