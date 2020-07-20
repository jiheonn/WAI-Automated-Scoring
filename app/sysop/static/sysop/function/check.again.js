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
    // currentTd.text("승인");
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
    // currentTd.text("승인");
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
    // currentTd.text("승인");
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
    // currentTd.text("승인");
});

$(".change_self_question").on('click', function () {
    let currentTd = $(this);
    let currentRow = currentTd.closest("tr");
    let td1 = currentRow.find("td:eq(1)").text();
    let td2 = currentRow.find("td:eq(2)").text();
    let td3 = currentRow.find("td:eq(3)").text();
    const data = '확인 선택시' + '\n' +
        '수정된 내용으로 문제가 변경됩니다.' + '\n' +
        '문제 정보를 변경하시겠습니까?';
    if (confirm(data) == true) {    //확인
        document.change_self_question_form.submit();
    } else {   //취소
        return false;
    }
    // currentTd.text("승인");
});