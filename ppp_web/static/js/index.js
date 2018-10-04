/*This file contains front-end application logic*/

// file select onchange event handler
function handleFileSelect(evt) {
  $.notifyClose();
  let file = evt.target.files[0];
  let reader = new FileReader();
  reader.onload = function(e) {
    let data = e.target.result;
    let workbook = XLSX.read(data, {
      type: 'binary'
    });
    let languageList = [];
    let defaultLanguage = '';
    workbook.SheetNames.forEach(function(sheetName) {
        let XL_row_object = XLSX.utils.sheet_to_json(workbook.Sheets[sheetName]);
        if (sheetName === 'choices') {
            $('#lang-picker').find('option').remove();
            const keys = Object.keys(XL_row_object[0]);
            keys.forEach(key => {
                if (key.startsWith('label::')) {
                    const l = key.substr(7);
                    languageList.push(l);
                    $('#lang-picker').append(new Option(l, l));
                }
            });
            
            if ($('#lang-picker option').length > 0) {
                $('#lang-picker').prop('disabled', false);
            } else {
                $('#lang-picker').append(new Option('No language specified in form.', 'none', true, true));
                setTimeout(() => {
                    $('#lang-picker').val('none');
                }, 1000);
                $('#lang-picker').prop('disabled', true);
            }
        }
        if (sheetName === 'settings') {
            defaultLanguage = XL_row_object[0].default_language;
        }
    });
    setDefaultLanguage(defaultLanguage, languageList);
  };
  reader.onerror = function(ex) {
    console.log('Exception: ', ex);
  };
  reader.readAsBinaryString(file);
}

function setDefaultLanguage(defaultLanguage, languageList) {
    if (defaultLanguage != null && defaultLanguage != '')
        $('#lang-picker').val(defaultLanguage);
    else if (languageList.indexOf('English') > -1)
        $('#lang-picker').val('English');
    else {
        languageList.sort();
        $('#lang-picker').val(languageList[0]);
    }
}

// function unchecks all checkboxes on the page
function clearOptions() {
    $("input[type='checkbox']").attr("checked", false);
}

// function checks input (radio button or checkbox) by value
function setOption(value) {
    let selector = "input[value='" + value + "']";
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
            return $.notify({
                message: 'Please, select file for uploading',
            }, {
                type: 'danger',
            });
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
            // $("#btnHtmlFormat").click();
            $("#btnDocFormat").click();
            
            // set default preset
            $("#btnDevPreset").click();
            
            // reset the form fields. here ".get(0)" will return a plain
            // javascript dom object instead of jquery object
            $("#form").get(0).reset();
        }, 3000)

    });

    /* preset button click event handler */
    // TODO: We will maybe add this later. I may delete this too. -jef 2018/09/25
    // $("#presets").find("label").click(function (event) {
    //     // get input element in clicked label
    //     let $e = $(event.target).find("input");
    //     // do nothing if custom button is clicked
    //     if ($e.val() === 'custom') {
    //         return;
    //     }
    //     // clear existing options
    //     clearOptions();
    //
    //     // enable options according to clicked preset
    //     switch ($e.val()) {
    //         case 'standard':
    //             break;
    //         case 'internal':
    //             setOption("hr-relevant");
    //             setOption("text-replacements");
    //             break;
    //         case 'public':
    //             setOption("input-replacement");
    //             setOption("exclusion");
    //             setOption("hr-relevant");
    //             setOption("hr-constraint");
    //             setOption("text-replacements");
    //             break;
    //         case 'detailed':
    //             setOption("input-replacement");
    //             setOption("exclusion");
    //             setOption("hr-relevant");
    //             setOption("hr-constraint");
    //             setOption("text-replacements");
    //             break
    //     }
    // });

    /* options checkbox click event handler */
    $("input[type='checkbox']").click(function (event) {
        // if any option is selected by user? automatically assume
        // that preset is "custom"
        $("#btnCustomPreset").click();
    });

    // when all the handlers configured, check if hidden container
    // contains a server message, and if contains, show it to user
    let $message = $("#message");
    let text = $message.text().trim();

    let notify_type;
    if ($message.data("category") == null) {
        notify_type = 'danger';
    } else {
        const arr_cat_type = {
            'error': 'danger',
            'warning': 'warning',
            'info': 'info'
        }
        notify_type = arr_cat_type[$message.data("category")];
    }

    if (text !== '') {
        $.notify({
            message: text,
        }, {
            element: '.submit-wrapper',
            type: notify_type,
            delay: 0,
            placement: {
                from: 'bottom',
                align: 'center'
            },
            position: 'relative',
            offset: {
                y: -20
            }
        });
    }
    
    // file input control change event handler
    document.getElementById('inFile').addEventListener('change', handleFileSelect, false);
});
