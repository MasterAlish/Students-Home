$(document).ready(function(){
    $(".delete-button").on("click", function () {
        return confirm($(this).data("delete-text")+"\nВы уверены что хотите удалить?");
    })
});
