function clearOptions() {
    $("input[type='checkbox']").attr("checked", false);
}

function setOption(value) {
    var selector = "input[value='" + value + "']";
    $(selector).prop('checked', true);
}

$(document).ready(function () {
    /* submit button click event handler */
    $("#btnSubmit").click(function (event) {
        if (!$("#inFile").val()) {
            event.preventDefault();
            return $(".file-input").notify("Please, select file for uploading", {
                position: "right",
                className: "error",
                autoHideDelay: 2000
            })
        }
        setTimeout(function () {
            $(event.target).prop("disabled", true);
        }, 100);
        setTimeout(function () {
            $(event.target).prop("disabled", false);
        }, 3000)

    });

    /* preset button click event handler */
    $("#presets").find("label").click(function (event) {
        var $e = $(event.target).find("input");
        if ($e.val() === 'custom') {
            return;
        }
        clearOptions();
        switch ($e.val()) {
            case 'developer':
                break;
            case 'internal':
                setOption("hr-relevant");
                setOption("text-replacements");
                break;
            case 'public':
                setOption("input-replacement");
                setOption("exclusion");
                setOption("hr-relevant");
                setOption("hr-constraint");
                setOption("text-replacements");
                break
        }
    });

    /* options checkbox click event handler */
    $("input[type='checkbox']").click(function (event) {
        $("#btnCustomPreset").click();
    });


    var $message = $("#message");
    var text = $message.text().trim();
    if (text !== '') {
        $.notify(text, {
            position: "top right",
            className: $message.data("category")
        })
    }
});