$(document).ready(function(){
    $(".delete-button").on("click", function () {
        return confirm("Вы уверены что хотите удалить?");
    })
});
