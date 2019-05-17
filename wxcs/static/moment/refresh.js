function update() {
  $('.drill-clock').html(moment().format('MMMM DD, YYYY // HH:mm:ss'));
}

setInterval(update, 1000);
