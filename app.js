var voteA = 0;
var voteB = 0;
var voteC = 0;

function displayVotes() {
  document.getElementById("vote-count-a").innerHTML = voteA;
  document.getElementById("vote-count-b").innerHTML = voteB;
  document.getElementById("vote-count-c").innerHTML = voteC;
}

window.onload = displayVotes;