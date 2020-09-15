var clip;
var timer;
var refresh;

$(document).ready(function(){

    $('button[name="newrun"]').hide();
    $('button[name="result"]').hide();

    $('button[name="newrun"]').click(function(){
        $.ajax({url:"do/new", async:false});
        location.reload();
    });

    $('button[name="result"]').click(function(){
        window.location.href = 'result.html';
    });


    clip = setInterval(function(){
        $('.badge').toggle();
    }, 500);


    var runtime;

    $.ajaxSetup({ cache: false });
    $.get('do/runtime', function(data){
        runtime=parseInt(data);
    });

    timer = setInterval(function(){
        runtime += 1;

        var hours = parseInt(runtime / 3600);
        var minutes = parseInt(runtime / 60) % 60;
        var seconds = runtime % 60;

        var s='';
        if (hours != 0) s+=' '+hours+' h';
        if (minutes != 0) s+=' '+minutes+' m';
        s+=' '+seconds+' s';

        $('#runtime').html(s);
    }, 1000);


    refresh = setInterval(f5, 3000);
    f5();
});

function f5()
{
    $.get('do/status', function(data){
        if (data == '')
        {
            $('.status').hide();
            clearTimeout(refresh);
            clearTimeout(timer);
            clearTimeout(clip);
        }
        else
        {
            $('.inputform').hide()

            if (data == 'Success')                  //Success
            {
                clearTimeout(refresh);
                clearTimeout(timer);
                clearTimeout(clip);
                $('#status').html('Finished');
                $('.status .progress-bar').removeClass('active');
                $('button[name="newrun"]').show();
                $('button[name="result"]').show();
            }
            else if (data == 'STARTED')             //Running
            {
                $('#status').html('Running');
            }
            else if (data == 'PENDING')             //Pending
            {
                $('#status').html('Pending');
            }
            else if (data[0] == 'E')                //Error
            {
                clearTimeout(refresh);
                clearTimeout(timer);
                clearTimeout(clip);
                $('.status table').hide();
                $('.progress').hide();

                $('.alert-info span').text(data);
                $(".alert-info").show();
                $('button[name="newrun"]').show();
            }
            else if (data[0] == 'P')                 //Processing
            {
                $('#status').html('Running');
                $('#log').show();
                $('#log pre').html(data);
            }
        }
    });

    $.get('do/queueStatus', function(data){
        if (data)
        {
            $('#total_worker').html(data['total_worker']);
            $('#active_task').html(data['active_task']);
            $('#reserved_task').html(data['reserved_task']);
        }
    }, 'json');
}

