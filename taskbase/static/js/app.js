$(function () {

    var t_id = $('#task_id'),
        c_name = $('#c_form #id_name'),
        c_category = $('#c_form #id_category'),
        c_deadline = $('#c_form #id_deadline_c'),
        c_priority = $('#c_form #id_priority'),
        c_notes = $('#c_form #id_notes'),
        u_name = $('#u_form #id_name'),
        u_notes = $('#u_form #id_notes'),
        u_category = $('#u_form #id_category'),
        u_deadline = $('#u_form #id_deadline_u'),
        u_priority = $('#u_form #id_priority'),
        u_completed = $('#u_form #id_completed'),
        u_btn =  $('#submit_u');

    u_btn.attr('disabled', true);

    c_name.on('click', function () {
        $(this).removeClass('field_required');
    });
    u_name.on('click', function () {
        $(this).removeClass('field_required');
    });

    function date_helper(s, t) {
        var fmt = t ? "YYYY-MM-DD H:mm:ss" : "YYYY-MM-DD";
        return (s === null ? '' : moment(s).format(fmt));
    }

    function bool_helper(b) {
        return (b === true ? 'Yes' : 'No');
    }

    function getTasks() {
        $.ajax({
            url: 'http://127.0.0.1:8000/tasks/',
            success: function (data) {
                var target = $('#tasks-table tbody');
                target.empty();
                $(data).each(function () {
                    var newTr = $('<tr data-id="' + this['id'] + '"></tr>');
                    newTr.append($('<td>' + this['name'] + '</td>'));
                    newTr.append($('<td>' + this['category'] + '</td>'));
                    newTr.append($('<td>' + date_helper(this['deadline'], false) + '</td>'));
                    newTr.append($('<td>' + this['priority'] + '</td>'));
                    newTr.append($('<td>' + bool_helper(this['completed']) + '</td>'));
                    newTr.append($('<td>' + date_helper(this['created'], true) + '</td>'));
                    newTr.append($('<td align="center"><button>Delete</button></td>'));
                    target.append(newTr);
                });
                var trs = $('#tasks-table tbody tr');
                trs.on('click', function () {
                    getTask($(this).data('id'));
                    trs.removeClass('highlight');
                    $(this).addClass('highlight');
                    t_id.data('id', $(this).data('id'));
                });
                $('button').on('click', function (e) {
                    e.stopPropagation();
                    delete_task($($(this).parents('tr')).data('id'));
                });
            }
        });
    }

    function getTask(task_id) {
        $.ajax({
            url: 'http://127.0.0.1:8000/tasks/' + task_id,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                u_name.removeClass('field_required');
                u_btn.attr('disabled', false);
                u_name.val(data['name']);
                u_notes.val(data['notes']);
                u_deadline.val(date_helper(data['deadline'], false));
                u_category.val(data['category']);
                u_priority.val(data['priority']);
                u_completed.attr('checked', data['completed']);
            }
        });
    }

    function delete_task(task_id) {
        $.ajax({
            url: 'http://127.0.0.1:8000/tasks/' + task_id + '/',
            type: 'DELETE',
            success: function () {
                getTasks();
            }
        });
    }

    $('#submit_c').on('click', function (e) {
        e.preventDefault();
        var data = {
            "name": c_name.val(),
            "category": c_category.val(),
            "deadline": c_deadline.val() === '' ? null : c_deadline.val() + 'T00:00',
            "priority": c_priority.val(),
            "notes": c_notes.val() === '' ? null : c_notes.val(),
            "completed": false,
            "creator": "user2"
        };

        c_name.val('');
        c_category.val('OT');
        c_deadline.val('');
        c_priority.val(4);
        c_notes.val('');

        if (data['name'].length > 0) {
            c_name.removeClass('field_required');
            $.ajax({
                url: 'http://127.0.0.1:8000/tasks/',
                data: data,
                type: 'POST',
                dataType: 'json',
                success: function (data) {
                    $(data).each(function () {
                        getTasks();
                    });
                }
            });
        } else {
            c_name.addClass('field_required');
        }
    });

    u_btn.on('click', function (e) {
        e.preventDefault();
        var data = {
            "name": u_name.val(),
            "category": u_category.val(),
            "deadline": u_deadline.val() === '' ? null : u_deadline.val() + 'T00:00',
            "priority": Number(u_priority.val()),
            "notes": u_notes.val() === '' ? null : u_notes.val(),
            "completed": u_completed[0].checked,
            "creator": "user2"
        };

        u_name.val('');
        u_category.val('OT');
        u_deadline.val('');
        u_priority.val(4);
        u_notes.val('');
        $(u_completed[0]).attr('checked', false);

        if (data['name'].length > 0) {
            u_btn.attr('disabled', true);
            $.ajax({
                url: 'http://127.0.0.1:8000/tasks/' + t_id.data('id') + '/',
                data: data,
                type: 'PUT',
                success: function () {
                    getTasks()
                },
            });
        } else {
            u_name.addClass('field_required');
        }
    });

    getTasks();

    $("#id_deadline_c").datepicker({
        dateFormat: "yy-mm-dd",
        showOtherMonths: true,
        selectOtherMonths: true,
        changeMonth: true,
        changeYear: true,
        showWeek: true,
    });

    $("#id_deadline_u").datepicker({
        dateFormat: "yy-mm-dd",
        showOtherMonths: true,
        selectOtherMonths: true,
        changeMonth: true,
        changeYear: true,
        showWeek: true,
    });
});