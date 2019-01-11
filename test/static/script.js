var buttons = []

$(document).ready(function() {
    $("time.timeago").timeago();
});
function selectBotVoice(){
    responsiveVoice.setDefaultVoice($(".selectbotvoice").val());
}
function sendRequest() {
    var user = "caesar"
    var entrypoint = "http://localhost:5005/conversations/default/respond?";
    // var query = entrypoint + "/conversations/" + user + "/respond?query=" + $("#btn-input").val();
    var querystring = $("#btn-input").val();
    var query = $("#btn-hidden-input").val();
    var person_query_html = '<li class="right clearfix">'+
            '<span class="chat-img pull-right"><img src="http://placehold.it/50/FA6F57/fff&text=ME" alt="User Avatar" class="img-circle" /></span>'+   
            '<div class="chat-body clearfix">'+
            '<div class="header">'+
                '<small class=" text-muted"><span class="glyphicon glyphicon-time"></span><time class="timeago" datetime="'+new Date()+'"></time></small>'+
                '<strong class="pull-right primary-font">Isopooh</strong>'+
            '</div>'+
            '<p class="pull-right">'+
                querystring +
            '</p>' +
        '</div>'+
            '</li><li class="waiting left clearfix">'+
            '<span class="waiting-img pull-left">'+
                '<img src="static/writing.gif" alt="Writing" class="img-writing" />'+
            '</span>'+
        '</li>'
    $(".chat").append(person_query_html);
    $('#btn-input').val("");
    var url = entrypoint + "query=" + query;

    var bot_answer_html =  '<li class="left clearfix"><span class="chat-img pull-left">'+
                                '<img src="http://placehold.it/50/55C1E7/fff&text=U" alt="User Avatar" class="img-circle" />'+
                                '</span>'+
                                '<div class="chat-body clearfix">'+
                                '<div class="header">'+
                                    '<strong class="primary-font">AI Bot</strong> <small class="pull-right text-muted">'+
                                    '<span class="glyphicon glyphicon-time"></span><time class="timeago" datetime="'+new Date()+'"></time></small>'+
                                '</div>'+
                                '<p>';


    $.getJSON(url, function(answers){
        if (answers.length>0){
            $.each(answers, function(i, answer){
                
                if (answer['text']){
                    bot_answer_html += answer['text'] + '<br/>';
                    responsiveVoice.speak(answer['text']);
                }
                if (answer['image'])
                    bot_answer_html += '<img class="chat-answer-img" src="'+ answer['image'] + '">' + '<br/>';
                if (answer['buttons']){
                    buttons = answer['buttons']
                    $.each(answer['buttons'], function(j, button){
                        bot_answer_html += '<button type="button" class="hotbtn btn btn-default" onclick="clickHotResponse('+j+')">' + button['title'] + '</button>';
                    })
                }

            });
        }
        else{
            bot_answer_html += "I can't know what you mean" + '<br/>';
        }

        bot_answer_html += '</p></div></li>';
        $(".waiting").remove();
        $(".chat").append(bot_answer_html);
        $("time.timeago").timeago();
   
       
    });    
}

function clickHotResponse(j){
    $("#btn-input").val(buttons[j]['title']);
    $("#btn-hidden-input").val(buttons[j]['payload']);
    $(".hotbtn").remove();
    buttons = [];
    sendRequest();
}
$('#btn-input').keypress(function(event){
	var keycode = (event.keyCode ? event.keyCode : event.which);
	if(keycode == '13'){
        $("#btn-hidden-input").val( $("#btn-input").val());
		sendRequest();
	}
});