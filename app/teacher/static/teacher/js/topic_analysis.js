var api_server = 'http://' + document.domain + ':' + 5252;

function getTopicModeling() {
    var csv_file = $("#topic-modeling-file")[0].files[0];
    var topic_count = document.getElementById("topic_count").value;

    if (!csv_file) { alert('파일을 업로드 해주세요.'); return; }
    if (csv_file.name.split('.').pop() !== 'csv' && csv_file.name.split('.').pop() !== 'xlsx') { alert('csv 파일 또는 엑셀 파일로 올려주세요.'); return; }
    if (topic_count > 50 || topic_count < 2) {
        alert("토픽 개수는 최소 2개, 최대 50개까지 입력이 가능합니다.");
        return false;
    }

    var form_data = new FormData();
    form_data.append('file', csv_file);
    form_data.append('num_topic', topic_count);
    $.ajax({
        url: api_server + '/get-topic-modeling',
        type: 'POST',
        dataType: 'json',
        processData: false,
        contentType: false,
        data: form_data,
        success: function(response) {
            id = response.id;
            console.log(id);
            res = response.data.df;
            console.log(res);
        }, error: function(e) { return; },
    });
}


$(document).ready(function () {
    $('#topic-modeling-submit-btn').click(function () {
        getTopicModeling();
    });    
});


/*
$(document).ready(function () {
    $('#response-analysis-submit-btn').click(function () {
        csv_file = $("#response-analysis-csv-file")[0].files[0];
        if (!csv_file) { alert('파일을 업로드 해주세요.'); return; }
        if (csv_file.name.split('.').pop() !== 'csv' && csv_file.name.split('.').pop() !== 'xlsx') { alert('csv 파일 또는 엑셀 파일로 올려주세요.'); return; }
        var file_data = new FormData();
        file_data.append('file', csv_file);
        $.ajax({
            url: api_server + '/analyze-response',
            type: 'POST',
            dataType: 'json',
            // crossDomain: true,
            processData: false,
            contentType: false,
            data: file_data,
            success: function(response) {
                id = response.id;
                console.log(id);
                res = response.data.df;
                console.log(res);
            }, error: function(e) { return; },
        });
    });
});
*/
