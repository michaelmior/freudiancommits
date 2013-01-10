$(function() {
  window.getIssue = function() {
    $.ajax({
      'url': '/github/randomissue/',
      'dataType': 'json',
      'success': function(data) {
        $('#github-issue').load('/github/issue/' + data.id + '/');
      },
      'error': function() {
        $('#github-issue').hide();
        $('.alert-error').show();
      }
    });
  };
  window.getIssue();
});
