(function showTime() {
  $('.drill-clock').html(moment().format('MMMM DD, YYYY // HH:mm:ss'));
  setTimeout(showTime, 1000);
})();
