$(document).ready(function () {
    $('#add-btn').click(function () {
        // count += 1;
        $('#questionTable').append(
            '<tr><td><textarea type="text" name="mark_text" placeholder="채점 준거를 작성해 주세요."></textarea></td></tr>'
        );
    });
});

$(document).ready(function () {
    $('#del-btn').click(function () {
        var my_tbody = document.getElementById('questionTable');
        var trCnt = $('#questionTable tr').length;
        if (trCnt >= 3) {
            if (my_tbody.rows.length < 1) return;
            my_tbody.deleteRow(my_tbody.rows.length - 1);
            // count -= 1;
        } else {
            alert("더 이상 삭제할 수 없습니다.");
            return false;
        }
    });
});

$(document).ready(function () {
    $('#make-btn').click(function () {
        var as_name = $('#as_name').val();
        var as_description = $('#as_description').val();
        var result = confirm("문항제목 : " + as_name + "\n문항내용 :\n" + as_description + "\n\n입력한 정보로 생성하겠습니까?");
        if (result) {
        } else {
            return false
        }
    });
});