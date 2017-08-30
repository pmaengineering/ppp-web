/*This file contains front-end application logic*/

// function unchecks all checkboxes on the page
function clearOptions() {
    $("input[type='checkbox']").attr("checked", false);
}

// function checks input (radio button or checkbox) by value
function setOption(value) {
    var selector = "input[value='" + value + "']";
    $(selector).prop('checked', true);
}

// add function, which will be ran when page is loaded. It will bootstrap
// page elements with events handlers
$(document).ready(function () {
    /* add submit button click event handler */
    $("#btnSubmit").click(function (event) {
        // if user has not selected a file
        if (!$("#inFile").val()) {
            // stop submitting form
            event.preventDefault();
            // show notification and exit handler
            return $(".file-input").notify("Please, select file for uploading", {
                position: "right",
                className: "error",
                autoHideDelay: 2000
            })
        }
        // disable submit button after 100 ms. to give form a chance to send
        // data to server
        setTimeout(function () {
            $(event.target).prop("disabled", true);
        }, 100);

        // clear the form after 3 seconds
        setTimeout(function () {
            // enable submit button
            $(event.target).prop("disabled", false);
            // set default output format
            $("#btnHtmlFormat").click();
            // set default preset
            $("#btnDevPreset").click();
            // reset the form fields. here ".get(0)" will return a plain
            // javascript dom object instead of jquery object
            $("#form").get(0).reset();
        }, 3000)

    });

    /* preset button click event handler */
    $("#presets").find("label").click(function (event) {
        // get input element in clicked label
        var $e = $(event.target).find("input");
        // do nothing if custom button is clicked
        if ($e.val() === 'custom') {
            return;
        }
        // clear existing options
        clearOptions();

        // enable options according to clicked preset
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
        // if any option is selected by user? automatically assume
        // that preset is "custom"
        $("#btnCustomPreset").click();
    });

    // when all the handlers configured, check if hidden container
    // contains a server message, and if contains, show it to user
    var $message = $("#message");
    var text = $message.text().trim();
    if (text !== '') {
        $.notify(text, {
            position: "top right",
            className: $message.data("category"),
            autoHideDelay: 5000
        })
    }
});