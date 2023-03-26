$(".voting-form").submit(function() {
  $("#loading-screen").show();
});
$(document).ajaxStop(function() {
  $("#loading-screen").hide();
});