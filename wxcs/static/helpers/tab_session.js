$('a[data-toggle="tab"]').click(function (e) {
  e.preventDefault();
  $(this).tab('show');
});

$('a[data-toggle="tab"]').on("shown.bs.tab", function (e) {
  var id = $(e.target).attr("href");
  sessionStorage.setItem('selectedTab', id)
});

var selectedTab = sessionStorage.getItem('selectedTab');
console.log(selectedTab);
if (selectedTab != null) {
  $('a[data-toggle="tab"][href="' + selectedTab + '"]').tab('show');
} else {
  $('a[data-toggle="tab"][href="#nav-log"]').tab('show');
}
