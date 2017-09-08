$(document).ready(function(){
    $(".delete-button").on("click", function () {
        if($(this).data("delete-text") != undefined){
            return confirm($(this).data("delete-text")+"\nВы уверены что хотите удалить?");
        }else{
            return confirm("Вы уверены что хотите удалить?");
        }
    })
});
