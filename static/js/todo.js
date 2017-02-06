Todo = {
    init: function () {
        $(".todo-delete").on("click", function () {
            var id = $(this).data("id");
            if (confirm("Вы уверены что хотите удалить?")) {
                $("#todo_form_id").val(id);
                $("#todo_form_action").val("delete");
                $("#todo_form").submit();
            }
        });
        $(".todo-check").on("click", function () {
            var id = $(this).data("id");
            if (confirm("Вы уверены что хотите изменить?")) {
                $("#todo_form_id").val(id);
                $("#todo_form_action").val("toggle");
                $("#todo_form").submit();
            }
        });
    }
};

$(document).ready(function () {
    Todo.init();
});