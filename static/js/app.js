$(document).ready(function() {
  const voteButton = document.querySelector('.vote-button');
  const confirmDialog = document.querySelector('#confirm-dialog');
  const yesButton = document.querySelector('.yes-button');
  const noButton = document.querySelector('.no-button');

  voteButton.addEventListener('click', function showpopup() {
    console.log('Click working');
    confirmDialog.style.display = 'block';
  });

  yesButton.addEventListener('click', function() {
    // Code for confirmed action goes here
    confirmDialog.style.display = 'none';
  });

  noButton.addEventListener('click', function() {
    confirmDialog.style.display = 'none';
  });
});