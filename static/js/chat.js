/**
 * Created by alisher on 9/24/16.
 */

var Chat = {
    messagesList: null,
    courseId: null,
    lastMessageId: 0,
    lastMessageDiv: null,
    messageInput: null,
    sound: null,

    init: function () {
        this.messagesList = $(".messages");
        this.courseId = this.messagesList.data("course-id");
        this.lastMessageId = this.messagesList.data("last-message-id");
        this.lastMessageDiv = $(".padding");
        this.messageInput = $("#message-input");
        this.startTimer();
        $("#new-message-submit").on("click", function(){
            var message = Chat.messageInput.val();
            Chat.postMessage(message);
            Chat.messageInput.val("")
            return false;
        });
        Chat.scrollToBottom();
        Chat.sound = $("#player");
    },

    startTimer: function () {
        setInterval(Chat.updateMessages, 3000);
    },

    playSound: function () {
        Chat.sound[0].play();
    },

    updateMessages: function () {
        $.ajax({
            url: "/chat/new-messages/",
            data:{
                course_id: Chat.courseId,
                last_message_id: Chat.lastMessageId
            }
        }).done(function (data) {
            Chat.lastMessageId = data.last_message_id;
            Chat.lastMessageDiv.before(data.new_messages);
            if(data.new_messages.length > 0){
                Chat.scrollToBottom();
                Chat.playSound();
            }
        }).fail(function (e) {
            console.log(e);
        });
    },

    postMessage: function(message){
        $.ajax({
            method: 'POST',
            url: "/chat/post/",
            data:{
                course_id: Chat.courseId,
                last_message_id: Chat.lastMessageId,
                message: message
            }
        }).done(function (data) {
            Chat.lastMessageId = data.last_message_id;
            Chat.lastMessageDiv.before(data.new_messages);
            Chat.scrollToBottom();
            Chat.playSound();
        }).fail(function (e) {
            console.log(e);
        });
    },

    scrollToBottom: function () {
        var scrollTop = Chat.messagesList.prop("scrollHeight") - Chat.messagesList.height();
        console.log("scroll: "+scrollTop);
        Chat.messagesList.animate({scrollTop: scrollTop}, "fast");
    }
};

$(document).ready(function () {
    Chat.init();
    setTimeout(Chat.scrollToBottom, 200);
});