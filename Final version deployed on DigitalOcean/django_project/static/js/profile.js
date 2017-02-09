/**
 * Created by raylu on 10/21/16.
 */
/**
 * Created by raylu on 10/21/16.
 */
function addComment(e) {
    e.preventDefault();
    button_id = e.target.id
    postid = button_id.substring(button_id.lastIndexOf('-')+1);
    content = $("#comment-input-"+postid).val();
    console.log('content:' + content + 'post_id: '+postid);
    $.post("addComment/", {comment: content, post_id: postid})
        .done(function (data) {
            console.log("enter addComment")
            var new_comment = data['html'];
            console.log(new_comment);
            console.log(data['post_id']);
            $("#comments-list-"+ data['post_id']).append(new_comment);
            $('#comment-input'+data['post_id']).val('');
        });
}

$(document).ready(function () {

  $('.btn-comment').click(addComment);

  // CSRF set-up copied from Django docs
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  });
});