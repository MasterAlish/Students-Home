var TabPills = {
    init: function () {
        $(".tab-pills").find("li>a").on("click", function () {
            var id = $(this).attr("href");

            $(".tab-pills").find("li").removeClass("active");
            $(this).closest("li").addClass("active");

            $(".tab-pill-tab").removeClass("active");
            $(id).addClass("active");

            return false;
        })
    }
};

var DeleteButton = {
    init: function () {
        $(".delete-button").on("click", function () {
            if ($(this).data("delete-text") != undefined) {
                return confirm($(this).data("delete-text") + "\nВы уверены что хотите удалить?");
            } else {
                return confirm("Вы уверены что хотите удалить?");
            }
        })
    }
};

$(document).ready(function () {
    TabPills.init();
    DeleteButton.init();
});
