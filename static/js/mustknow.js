MustKnow = {
    init: function () {
        $(".must-know-item .item-check").on("click", function () {
            var parent = $(this).parent();
            var url = parent.data("url");
            $.ajax({
                url: url
            }).done(function (data) {
                var counter = $(".must-knows-progress .done");
                if(data.done){
                    $(parent).addClass("done");
                    $(parent).find(".fa").removeClass("fa-square-o").addClass("fa-check-square-o")
                    counter.text(parseInt(counter.text())+1);
                }else{
                    $(parent).removeClass("done");
                    $(parent).find(".fa").addClass("fa-square-o").removeClass("fa-check-square-o")
                    counter.text(parseInt(counter.text())-1);
                }
            });
        });

        $(".add_item").on("submit", function(){
            var name = $(this).find("#item_name").val();
            var url = $(this).data("url");
            var form = $(this);
            $.ajax({
                url: url,
                data: {'name': name}
            }).done(function(html){
                form.before(html);
            });
            return false;
        });

        $(document).on("click", ".must-know-item .up", function(){
            var item = $(this).closest(".must-know-item");
            var url = item.data("action-url");
            $.ajax({
                url: url,
                data: {'action': 'up'}
            }).done(function(html){
                var newItem = item.clone();
                item.prev().before(newItem);
                item.remove();
            });
            return false;
        });

        $(document).on("click", ".must-know-item .down", function(){
            var item = $(this).closest(".must-know-item");
            var url = item.data("action-url");
            $.ajax({
                url: url,
                data: {'action': 'down'}
            }).done(function(html){
                var newItem = item.clone();
                item.next().after(newItem);
                item.remove();
            });
            return false;
        });
    }
};

$(document).ready(function () {
    MustKnow.init();
});