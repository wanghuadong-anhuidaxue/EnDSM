$(document).ready(function(){

    $(".alert-info").hide();

    $('#uploadvar').click(function(){
        $('input[name="varfile"]').click();
    });

    $('input[name="varfile"]').change(function(){
        $('textarea[name="vars"]').attr('placeholder', $('input[name="varfile"]').val());
    });

    $('#target').on('switch-change', function(event, data){
        $('select[name="type"]').parent().parent().toggle();
    });


    $('#example').click(function(){
        $.get('do/example/1', function(data){
            $('textarea[name="vars"]').val(data['var']);
        }, 'json');
    });


    $('button[name="submit"]').click(function(){
        if (checkForm()){

            $('#uploadproc').modal({backdrop: 'static', keyboard: 'false'});

            $.ajax({url:"do/new", async:false});

            post_init();
            $('form').ajaxSubmit({
                url: "do/submit",
                type: "POST",
                uploadProgress: function(event, position, total, percentComplete) {
                    var percentVal = percentComplete + '%';
                    $('.progress-bar').width(percentVal);
                    $('.modal span').text('Uploading '+percentVal)
                    if (percentComplete == 100)
                        $('.modal span').text('Parsing, please wait ... ')
                },
                success: function(data){
                    $.ajax({url:"do/run", method:"POST"}).done(function(){
                        $('#uploadproc').modal('hide');
                        window.location.href='index.html';
                    });
                }
            });

        }
    });

});


function checkForm()
{
    $(".alert-info").hide();

    var vars = $('textarea[name="vars"]').val();
    var varfile = $('input[name="varfile"]').val();

    if (vars == "" && varfile == "")
    {
        $('.alert-info span').text("Please input variants or upload a file.");
        $(".alert-info").show();
        return false;
    }

    return true;
}


