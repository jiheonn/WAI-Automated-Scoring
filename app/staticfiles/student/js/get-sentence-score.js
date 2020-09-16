// 피드백 결과 탭 이동 함수
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

// 문장 채점 함수
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
            if (0 <= result && result < 0.046) {
                standard_answer = "핵심어를 사용하여 완결된 문장으로 답안을 잘 작성해 보세요."
            }
            else if (0.046 <= result && result < 0.08) {
                standard_answer = "잘 작성했어요. 혹시 주어, 서술어, 목적어 등 문장의 주요 성분이 빠진 것은 없는지 다시 한 번 점검해 보세요."
            }
            else {
                standard_answer = "좋은 문장으로 정말 잘 작성했어요."
            }

            $("div").remove("#whole_result");
            $("#calculated_score").after('<div id="whole_result">' + '</div>');
            $("#whole_result").append(
                '<p>' +
                standard_answer +
                '</p>' +
                '<p>' +
                '문장 점수 : ' +
                '<b id="sentence_score" value="' +
                result +
                '">' +
                result +
                '</b>' +
                ' 점' +
                '<br/>' +
                '개념 점수 : ' +
                '<b>' +
                result +
                '</b>' +
                ' 점' +
                '</p>'
            );
            hide_button();
        }, error: function (e) { return; },
    });
});

// 점수 미달시 다음 문항 이동 불가
function hide_button() {
    var sentence_score = document.getElementById('sentence_score').innerText;

    if (sentence_score < 0.08) {
        $('#question_id').attr('hidden', true);
    }
} 


// var api_server = 'http://' + document.domain + ':' + 5000;

// $(document).ready(function () {
//     // var ml_model = $('#ml_model_check');
//     // var question_id = $('#ml_model_check');
//     // var score = $('#score');
    
//     input_text = $('#question_answer').text();
//     // console.log(input_text);
//     var form_data = new FormData();
//     form_data.append('sentence', input_text);
//     $.ajax({
//         url: api_server,
//         type: 'POST',
//         dataType: 'json',
//         processData: false,
//         contentType: false,
//         data: form_data,
//         success: function (response) {
//             if (response.id == "scoring-api") {
//                 result = response.data.score;
//                 console.log(result); // 문장의 점수 출력
//             } else {
//                 alert('error!');
//                 return;
//             }

//             $("div").remove("#logo_say");
//             $("#logo_after").after('p class="font-weight-bolder triangle-border left" id="logo_say">' + '</p>');

//             if (score == 1){
//                 $("#logo_say").append(
//                     'p class="font-weight-bolder triangle-border left" id="logo_say">' +
//                     '참 잘 설명했어요!' +
//                     '</p>'
//                 );
//             }
//             else {
//                 $("div").remove("#logo_say");
//                 $("#logo_after").after(
//                     'p class="font-weight-bolder triangle-border left" id="logo_say">' +
//                     '다시 한번 설명해볼까요?' +
//                     '</p>'
//                 );
//             }

            
//             hide_button();
//         }, error: function (e) { return; },
//     });
// });