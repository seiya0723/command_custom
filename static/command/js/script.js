//Forbidden対策として予めAjaxを送信前にセットする。

//Ajax実行前にセッションIDを送信するスクリプト
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
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
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }   
});



window.addEventListener("load" , function (){

    $(".file_command_submit").on("click", function() { command_send(this); });

});

function command_send(elem){

    //Ajaxで送信する時、任意の値をセットして送信。FormData形式
    //https://noauto-nolife.com/post/javascript-formdata-obj-set/

    let form_elem   = $(elem).parent();
    let url         = form_elem.prop("action");
    let method      = form_elem.prop("method");

    let command = form_elem.children(".file_command_name").val() + " " + form_elem.children(".file_command_args").val();

    let data    = new FormData();
    data.set("command", command);

    $.ajax({
        url: url,
        type: method,
        data: data,
        processData: false,
        contentType: false,
        dataType: 'json'
    }).done( function(data, status, xhr ) { 
        
        if (data.json_data){
            console.log("送信失敗");
        }
        else{
            console.log("送信成功");
        }
    }).fail( function(xhr, status, error) {
        console.log("エラー");
    }); 



}



