(function pollTasks() {
  fetch(Flask.url_for('core.tasks')).then(function (response) {
    return response.json();
  }).then(function (json) {
    // TODO: Perform render task to DOM
    console.log(json);
  });
  setTimeout(pollTasks, 1000 * 120); // Can change the time interval here
})();
