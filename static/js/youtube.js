window.onscroll = function(ev) {

    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
        var token = "{{token}}"
        console.log(token)
        $.ajax({
        type: "POST",
        url: "{% url youtube_page %}",
        data: {
            'nextPagetoken': token,
        },
        success: function(html)
        {
            alert(html);
        }
        });
    }
};