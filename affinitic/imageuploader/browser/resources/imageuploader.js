jQuery(document).ready(function($) {

    $('#fileupload').fileupload({
        url: 'upload-image',
        dataType: 'json',
        done: function (e, data) {
            if (data.result.status == -1)
            {
                $("#error-message").text(data.result.message);
                $("#error-message").show();
            }
            else {
                $("#image-edition-fieldset").load("crop-image", {'filename': data.result.filename,
                                                                 'desiredHeight': data.result.desiredHeight,
                                                                 'desiredWidth': data.result.desiredWidth,
                                                                 'height': data.result.height,
                                                                 'width': data.result.width,
                                                                 'destination': data.result.destination,
                                                                 'redirectUrl': data.result.redirectUrl,
                                                                 'layoutmaxwidth': data.result.layoutmaxwidth,
                                                                 'status': data.result.status,
                                                                 'message': data.result.message});
            }
        },
        progressall: showProgress
    });
});


function showProgress(e, data) {
    $("#error-message").hide();
    $("#progress").show();
    var progress = parseInt(data.loaded / data.total * 100, 10);
    var percentVal = progress + '%';
    $('#progress .bar').css(
        'width',
        progress + '%'
    );
    $('#progress .bar').html(percentVal);
};

function checkCoords() {
    if (parseInt($('#w').val(), 10) > 0) return true;
    alert("Veuillez d'abord couper l'image avant de la sauvegarder.");
    return false;
};
