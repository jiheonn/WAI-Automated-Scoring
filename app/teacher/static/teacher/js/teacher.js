$(function () {
    var current = location.pathname;
    $('#menubar li a').each(function () {
        var $this = $(this);
        // if the current path is like this link, make it active
        if ($this.attr('href').indexOf(current) !== -1) {
            $this.parents('li').addClass('active');
        }
    });
});

// var count = 1;
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
        var as_discription = $('#as_discription').val();
        var result = confirm("문항제목 : " + as_name + "\n문항내용 :\n" + as_discription + "\n\n입력한 정보로 생성하겠습니까?");
        if (result) {
        } else {
            return false
        }
    });
});

$(document).ready(function () {
    $('.qr-button').on('click', (e) => {
        var question_name = e.target.value;
        alert(question_name);
        $.ajax({
            url: '/teacher/change_qr_code/',
            data: { question_name: question_name },
            success: function (data) {
                var question_data = data.question_data;
                var num = question_data.length;
                $('#QR_code_img').remove();
                for (var i = 0; i < num; i++) {
                    $("#img_space").append(
                        '<img id="QR_code_img" src="' +
                        '/media/'
                        + question_data[i].QR_code +
                        '">'
                    );
                }
            }
        });
    });
});
jQuery(function ($) {
    /* Checkbox  */
    var checkBox = $('.ctm-check');
    var addClassCheckBox = function ($input) {
        if ($input.prop('checked')) {
            $input.parent().addClass('checked');
        } else {
            $input.parent().removeClass('checked');
        }
    };
    checkBox.on('change', 'input', function () {
        addClassCheckBox($(this));
    })
});
$(document).ready(function () {
    $('#copy').click(function () {
        var copy_code = prompt("복사할 시험지의 코드를 입력해 주세요.");
        $.ajax({
            url: '/teacher/assignment_copy/',
            data: { copy_code: copy_code },
            success: function (data) {
                var copy_data = data.copy_data;
                var num = copy_data.length;
                if (num == 0) {
                    if (copy_code) {
                        alert('시험지가 존재하지 않습니다. 코드를 다시 확인해 주세요.');
                    }
                } else {
                    for (var i = 0; i < num; i++) {
                        var assignment_type = copy_data[i].assignment_type;
                        var assignment_title = copy_data[i].assignment_title;
                        var question_id = copy_data[i].question_id;
                        $('#evaluation_type').val(assignment_type).prop("selected", true);
                        $('#as_name').val(assignment_title);
                        $('input:checkbox[id=' + question_id + ']').prop("checked", true);
                        $('#' + copy_data[i].question_id).addClass("checked");
                    }
                }
                jQuery(function ($) {
                    /* Checkbox  */
                    var checkBox = $('.ctm-check');
                    var addClassCheckBox = function ($input) {
                        if ($input.prop('checked')) {
                            $input.parent().addClass('checked');
                        } else {
                            $input.parent().removeClass('checked');
                        }
                    };
                    checkBox.on('change', 'input', function () {
                        addClassCheckBox($(this));
                    })
                });
            }
        })
    })
});

$(document).ready(function () {
    $('#input_text').keyup(function () {
        if ($(this).val().length > $(this).attr('maxlength')) {
            alert('입력 제한 길이를 초과하였습니다.');
            $(this).val($(this).val().substr(0, $(this).attr('maxlength')));
        }
    });
});

$(document).ready(function () {
    $('#code_num').keyup(function () {
        if ($(this).val().length > $(this).attr('maxlength')) {
            alert('최대 8자리 입력을 초과하였습니다.');
            $(this).val($(this).val().substr(0, $(this).attr('maxlength')));
        }
    });
});

$(document).ready(function () {
    $('#make-submit').click(function () {
        var code_num = $('#code_num').val();
        var as_name = $('#as_name').val();
        var type = $('#evaluation_type option:selected').val();
        var check_num = $('input:checked').length;
        var st_date = $('#start-date').val();
        var en_date = $('#end-date').val();
        var result = confirm("코드 : " + code_num + "\n시험지 제목 : " + as_name + "\n타입 : " + type + "\n문항 수 : " + check_num + "\n시작날짜 : " + st_date + "\n종료날짜 : " + en_date + "\n\n입력한 정보로 생성하겠습니까?");
        if (result) {
        } else {
            return false
        }
    });
});

$(document).ready(function () {
    $('#code_generate').click(function () {
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

        for (var i = 0; i < 8; i++)
            text += possible.charAt(Math.floor(Math.random() * possible.length));

        $.ajax({
            url: '/teacher/code_generation/',
            data: { text: text },
            success: function (data) {
                $('#code_num').val(data.generation_code);
            }
        });
    });
});

$(document).ready(function () {
    $('#search').click(function () {
        var user_input = $('#user_input').val();
        $.ajax({
            url: '/teacher/question_search/',
            data: { user_input: user_input },
            success: function (data) {
                var search_data = data.search_data;
                var num = search_data.length;
                if (num == 0) {
                    alert('검색 결과가 존재하지 않습니다.');
                } else {
                    $("div").remove("#question_list");
                    $("#category_option").after('<div id="question_list" class="row qstlst-margin">' + '</div>');
                    for (var i = 0; i < num; i++) {
                        $("#question_list").append(
                            '<div class="col-md-3 mb-5">' +
                            '<div class="card h-100" align="center">' +
                            '<div class="card-body">' +
                            '<img class="img-fluid rounded mb-4 mb-lg-0 question-img" src="' +
                            '/media/' +
                            search_data[i].question_image +
                            '">' +
                            '</div>' +
                            '<span class="card-footer ctm-check">' +
                            '<input type="checkbox" id="' +
                            search_data[i].question_id +
                            '" name="question" value="' +
                            search_data[i].question_id +
                            '">' +
                            '<label for="' +
                            search_data[i].question_id +
                            '"><i></i>' +
                            search_data[i].question_name +
                            '</label>' +
                            '</span>' +
                            '</div>' +
                            '</div>'
                        )
                    }
                }
                jQuery(function ($) {
                    /* Checkbox  */
                    var checkBox = $('.ctm-check');
                    var addClassCheckBox = function ($input) {
                        if ($input.prop('checked')) {
                            $input.parent().addClass('checked');
                        } else {
                            $input.parent().removeClass('checked');
                        }
                    };
                    checkBox.on('change', 'input', function () {
                        addClassCheckBox($(this));
                    })
                });
            }
        });
    });
});

$(document).ready(function () {
    $('#category_option').change(function () {
        var option = $("#category_option option:selected").val();
        $.ajax({
            url: '/teacher/change_category/',
            data: { option: option },
            success: function (data) {
                var option_data = data.option_data;
                var num = option_data.length;
                $("div").remove("#question_list");
                $("#category_option").after('<div id="question_list" class="row qstlst-margin">' + '</div>');
                for (var i = 0; i < num; i++) {
                    $("#question_list").append(
                        '<div class="col-md-3 mb-5">' +
                        '<div class="card h-100" align="center">' +
                        '<div class="card-body">' +
                        '<img class="img-fluid rounded mb-4 mb-lg-0 question-img" src="' +
                        '/media/' +
                        option_data[i].question_image +
                        '">' +
                        '</div>' +
                        '<span class="card-footer ctm-check">' +
                        '<input type="checkbox" id="' +
                        option_data[i].question_id +
                        '" name="question" value="' +
                        option_data[i].question_id +
                        '">' +
                        '<label for="' +
                        option_data[i].question_id +
                        '"><i></i>' +
                        option_data[i].question_name +
                        '</label>' +
                        '</span>' +
                        '</div>' +
                        '</div>'
                    )

                }
                jQuery(function ($) {
                    /* Checkbox  */
                    var checkBox = $('.ctm-check');
                    var addClassCheckBox = function ($input) {
                        if ($input.prop('checked')) {
                            $input.parent().addClass('checked');
                        } else {
                            $input.parent().removeClass('checked');
                        }
                    };
                    checkBox.on('change', 'input', function () {
                        addClassCheckBox($(this));
                    })
                });
            }
        })
    })
});

$(document).ready(function () {
    $('#asi_info').DataTable();
});

var message = $('#message').val();
if (message.length) {
    alert(message);
}
