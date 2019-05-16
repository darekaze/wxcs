var datetime = null,
    date = null;

var update = function () {
    date = moment(new Date())
    datetime.html(date.format('MMMM DD, YYYY // HH:mm:ss'));
};

$(document).ready(function(){
    datetime = $('.drill-clock')
    update();
    setInterval(update, 1000);
});
