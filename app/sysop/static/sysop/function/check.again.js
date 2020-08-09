$(".approve-ok").on('click', function () {
    let currentTd = $(this);
    let currentRow = currentTd.closest("tr");
    let td1 = currentRow.find("td:eq(1)").text();
    let td2 = currentRow.find("td:eq(2)").text();
    let td3 = currentRow.find("td:eq(3)").text();
    const data = '이름 : ' + td1 + '\n' +
        '학교 : ' + td2 + '\n' +
        '이메일 : ' + td3 + '\n\n' +
        '선생님을 승인하시겠습니까?';
    if (confirm(data) == true) {    //확인
        document.change_approve_ok.submit();
    } else {   //취소
        return false;
    }
});

$(".approve-cancel").on('click', function () {
    let currentTd = $(this);
    let currentRow = currentTd.closest("tr");
    let td1 = currentRow.find("td:eq(1)").text();
    let td2 = currentRow.find("td:eq(2)").text();
    let td3 = currentRow.find("td:eq(3)").text();
    const data = '이름 : ' + td1 + '\n' +
        '학교 : ' + td2 + '\n' +
        '이메일 : ' + td3 + '\n\n' +
        '선생님 승인을 취소하시겠습니까?';
    if (confirm(data) == true) {    //확인
        document.change_approve_cancel.submit();
    } else {   //취소
        return false;
    }
});

$(".upload-self-ok").on('click', function () {
    let currentTd = $(this);
    let currentRow = currentTd.closest("tr");
    let td1 = currentRow.find("td:eq(1)").text();
    let td2 = currentRow.find("td:eq(2)").text();
    let td3 = currentRow.find("td:eq(3)").text();
    const data = '문항명 : ' + td1 + '\n' +
        '등록자 : ' + td2 + '\n' +
        '최초등록일자 : ' + td3 + '\n\n' +
        '문항을 등록하시겠습니까?';
    if (confirm(data) == true) {    //확인
        document.change_approve_ok.submit();
    } else {   //취소
        return false;
    }
});

$(".upload-self-cancel").on('click', function () {
    let currentTd = $(this);
    let currentRow = currentTd.closest("tr");
    let td1 = currentRow.find("td:eq(1)").text();
    let td2 = currentRow.find("td:eq(2)").text();
    let td3 = currentRow.find("td:eq(3)").text();
    const data = '문항명 : ' + td1 + '\n' +
        '등록자 : ' + td2 + '\n' +
        '최초등록일자 : ' + td3 + '\n\n' +
        '문항등록을 취소하시겠습니까?';
    if (confirm(data) == true) {    //확인
        document.change_approve_cancel.submit();
    } else {   //취소
        return false;
    }
});

$(".change_self_question").on('click', function () {
    const data = '확인 선택시' + '\n' +
        '수정된 내용으로 문제가 변경됩니다.' + '\n\n' +
        '문제 정보를 변경하시겠습니까?';
    if (confirm(data) == true) {    //확인
        document.change_self_question_form.submit();
    } else {   //취소
        return false;
    }
});

$(".change_question").on('click', function () {
    const data = '확인 선택시' + '\n' +
        '수정된 내용으로 문제가 변경됩니다.' + '\n\n' +
        '문제 정보를 변경하시겠습니까?';
    if (confirm(data) == true) {    //확인
        document.change_question_form.submit();
    } else {   //취소
        return false;
    }
});

$(".change_notice").on('click', function () {
    const data = '확인 선택시' + '\n' +
        '수정된 내용으로 공지사항이 변경됩니다.' + '\n\n' +
        '공지사항을 변경하시겠습니까?';
    if (confirm(data) == true) {    //확인
        document.change_notice_form.submit();
    } else {   //취소
        return false;
    }
});

$(".delete_question_btn").on('click', function () {
    let currentTd = $(this);
    let currentRow = currentTd.closest("tr");
    let td1 = currentRow.find("td:eq(1)").text();
    let td2 = currentRow.find("td:eq(2)").text();
    const data = '확인 선택시' + '\n' +
        '문항명 : ' + td1 + '\n' +
        '최초등록일자 : ' + td2 + '\n\n' +
        '해당 문항이 삭제되며\n' +
        '문항 관련된 데이터가 모두 삭제됩니다.';
    if (confirm(data) == true) {    //확인
        document.delete_question_form.submit();
    } else {   //취소
        return false;
    }
});

$(".delete_notice_btn").on('click', function () {
    let currentTd = $(this);
    let currentRow = currentTd.closest("tr");
    let td1 = currentRow.find("td:eq(1)").text();
    let td2 = currentRow.find("td:eq(2)").text();
    const data = '확인 선택시' + '\n' +
        '공지사항 제목 : ' + td1 + '\n' +
        '최초등록일자 : ' + td2 + '\n\n' +
        '해당 공지사항이 삭제됩니다.';
    if (confirm(data) == true) {    //확인
        document.delete_notice_form.submit();
    } else {   //취소
        return false;
    }
});