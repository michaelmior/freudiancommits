$(function() {
  $.ajax({
    'url': '/github/fetch_data/',
    'dataType': 'json',
    'timeout': 30000,
    'success': function() {
      window.setTimeout(function() {
        window.location = '/';
      }, 1000);
    },
    'error': function() {
      $('.loading').hide();
      $('.alert-error').show();
    }
  });
});
