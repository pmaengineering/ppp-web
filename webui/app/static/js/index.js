function clearOptions() {
    $("input[type='checkbox']").attr("checked", false);
}

function setOption(value) {
    var selector = "input[value='" + value + "']";
    $(selector).click();
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
    });

    /* preset button click event handler */
    $("#presets").find("label").click(function (event) {
        var $e = $(event.target).find("input");
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
        $("#presets").find("input").attr("checked", false);
    });
});