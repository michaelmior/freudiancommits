$(function() {
  window.getIssue = function() {
    $.getJSON('/github/randomissue/', function(data) {
      $('#github-issue').load('/github/issue/' + data.id + '/');
    });
  };
  window.getIssue();
});
