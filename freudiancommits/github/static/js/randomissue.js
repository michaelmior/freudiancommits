$(function() {
  var loading = false;

  window.getIssue = function() {
    if (loading) return;
    loading = true;

    $.ajax({
      'url': '/github/randomissue/',
      'dataType': 'json',
      'success': function(data) {
        loading = false;
        $('#github-issue').load('/github/issue/' + data.id + '/');
      },
      'error': function() {
        loading = false;
        $('#github-issue').hide();
        $('.alert-error').show();
      }
    });
  };
  window.getIssue();
});
