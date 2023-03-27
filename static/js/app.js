function show() {
  // code to show the animation goes here
  $(".coffee-container").show();
  $(".coffee-header").show();
  $(".coffee-medium").show();
  $(".coffee-footer").show();
  $(".loading-screen-text").show();
 
  console.log("Animation shown");
}

$(document).ready(function() {

  // Hide the animation elements initially
  $(".coffee-container").hide();
  $(".coffee-header").hide();
  $(".coffee-medium").hide();
  $(".coffee-footer").hide();
  $(".loading-screen-text").hide();

  $(".voting-form").submit(function(event) {
    //event.preventDefault(); // prevent form from submitting
    show(); // call show function when form is submitted
  });

  $(document).ajaxStop(function() {
    $(".coffee-container").hide();
    $(".coffee-header").hide();
    $(".coffee-medium").hide();
    $(".coffee-footer").hide();
    $(".loading-screen-text").hide();
  });

});