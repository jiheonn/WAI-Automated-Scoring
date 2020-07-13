$(".approve-ok").on('click', function () {
    let currentTd = $(this);
    let currentRow = currentTd.closest("tr");
    let td1 = currentRow.find("td:eq(1)").text();
    let td2 = currentRow.find("td:eq(2)").text();
    let td3 = currentRow.find("td:eq(3)").text();
    const data = '이름 : ' + td1 + '\n' +
        '학교 : ' + td2 + '\n' +
        '이메일 : ' + td3 + '\n' +
        '승인하시겠습니까?';
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
        '이메일 : ' + td3 + '\n' +
        '승인을 취소하시겠습니까?';
    if (confirm(data) == true) {    //확인
        document.change_approve_cancel.submit();
    } else {   //취소
        return false;
    }
    // currentTd.text("승인");
});