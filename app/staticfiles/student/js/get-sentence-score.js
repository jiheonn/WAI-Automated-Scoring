function openCity(evt, cityName) {
    var i, x, tablinks;
    x = document.getElementsByClassName("city");
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < x.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" w3-indigo", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " w3-indigo";
}

var api_server = 'http://' + document.domain + ':' + 5252; // sentence-analysis 서버의 포트로 수정

$(document).ready(function () {
    input_text = $('#question_answer').text();
    console.log(input_text);
    var form_data = new FormData();
    form_data.append('sentence', input_text);
    $.ajax({
        url: api_server + '/get-sentence-score',
        type: 'POST',
        dataType: 'json',
        processData: false,
        contentType: false,
        data: form_data,
        success: function (response) {
            if (response.id == "get-sentence-score") {
                result = response.data.score;
                console.log(result); // 문장의 점수 출력
            } else {
                alert('error!');
                return;
            }
            if (0 <= result < 0.046) {
                standard_answer = "핵심어를 사용하여 완결된 문장으로 답안을 잘 작성해 보세요."
            }
            else if (0.046 <= result < 0.08) {
                standard_answer = "잘 작성했어요. 혹시 주어, 서술어, 목적어 등 문장의 주요 성분이 빠진 것은 없는지 다시 한 번 점검해 보세요."
            }
            else {
                standard_answer = "좋은 문장으로 정말 잘 작성했어요."
            }

            $("div").remove("#whole_result");
            $("#calculated_score").after('<div id="whole_result">' + '</div>');
            $("#whole_result").append(
                '<p>' +
                '<b>' +
                result +
                '</b>' +
                ' 점' +
                '</p>' +
                '<p>' +
                standard_answer +
                '</p>'
            )
        }, error: function (e) { return; },
    });
});