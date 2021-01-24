$('document').ready(function () {
    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
    var csrftoken = getCookie('csrftoken');
    $('.like-comment').on('click', function() {
        console.log('hello')
        let id=$(this).attr('id');
        let current_id = id.split('-')[1];
        $.ajax({
            url:`/shop/add_like2comment_ajax/${current_id}`,
            headers: {"X-CSRFToken": csrftoken},
            method: "PUT",
            success: function (data) {
                $(`#${id}`).html(`Likes: ${data['likes']}`);
            }
        })
    });

    $('.delete-comment').on('click', function() {
        let id=$(this).attr('id');
        let comment_id = id.split('-')[2];
        $.ajax({
            url:`/shop/delete_comment_ajax/${comment_id}`,
            headers: {"X-CSRFToken": csrftoken},
            method: "DELETE",
            success: function (data) {
                $(`#${id}`).remove();
            }
        })
    });
    $('.delete-book').on('click', function() {
        var id=$(this).attr('id');
        $.ajax({
            url:"/shop/delete_book_ajax",
            data: {'slug': id.split('_')[2]},
            method: "GET",
            success: function (data) {
                $(`#${id}`).remove();
            }
        })
    });
    $('span.rate').on('click', function() {
        let id=$(this).attr('id');
        $.ajax({
            url:"/shop/add_rate_ajax",
            data: {'slug': id.split('_')[1], 'rate': id.split('_')[2]},
            method: "GET",
            success: function (data) {
                let b_slug = id.split('_')[1]
                $(`#book_rate_${b_slug}`).html(`Rate: ${data['rate']}`)
                for (let i = 1; i < 6; i++) {
                        if (i <= data['rate']){
                            $(`#book_${b_slug}_${i}`).attr('class', 'rate fa fa-star checked')
                        }else{
                            $(`#book_${b_slug}_${i}`).attr('class', 'rate fa fa-star')}
                     }
            }
        })
    });
    $('.form-comment').on('submit', function(event) {
        var book_slug = $(this).attr('id')
        event.preventDefault();
        console.log('form submitted!');
        console.log(book_slug)
        console.log($('#comment-text').val())
        $.ajax({
            url:"/shop/add_comment_ajax",
            headers: { "X-CSRFToken": csrftoken },
            data: {
                'new_comment': $('#comment-text').val(),
                'slug': book_slug,
                },
            method: "POST",
            success: function (json) {
                console.log(json);
                $('#comment-text').val('');
                $('#bookdetailview').prepend('<h3 class="mb-0">' + json.text + '</h3>');
            }
        })

    });

})