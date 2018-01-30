/**
 * Created by alisher on 3/12/17.
 */

function addClassToInputs(form_id) {
    $(document).ready(function () {
        var form = $("#" + form_id);
        form.find("input").each(function () {
            if (this.type != 'submit' && this.type != 'checkbox')
                $(this).addClass("form-control");
        });
        form.find("textarea").each(function () {
            $(this).addClass("form-control");
        });
        form.find("select").each(function () {
            $(this).addClass("form-control");
        });
    });
}

function addDatePicker(ids) {
    $(document).ready(function () {
        try {
            for (var i = 0; i < ids.length; i++) {
                var date_input = $("#" + ids[i]);
                date_input.datepicker({
                    'format': "dd.mm.yyyy"
                });
                date_input.css("max-width", "200px");
                date_input.css("line-height", "1em");
            }
        }catch(e){}
    });
}
