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
        u_btn = $('#submit_u'),
        c_cancel = $('#cancel_c'),
        u_cancel = $('#cancel_u'),
        u_form_fields = [u_name, u_notes, u_deadline, u_category, u_priority, u_completed, u_btn];

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
        return (b === true ? '<i class="far fa-check-square"></i>' : '<i class="far fa-square"></i>');
    }

    function reset_form(f_name) {
        if (f_name === 'u_form') {
            u_name.val('');
            u_category.val('OT');
            u_deadline.val('');
            u_priority.val(4);
            u_notes.val('');
            $(u_completed[0]).prop('checked', false);
        } else if (f_name === 'c_form') {
            c_name.val('');
            c_category.val('OT');
            c_deadline.val('');
            c_priority.val(4);
            c_notes.val('');
        }
    }

    function disable_update_form_fields() {
        $(u_form_fields).each(function () {
            $(this).attr('disabled', true);
        });
    }

    function enable_update_form_fields() {
        $(u_form_fields).each(function () {
            $(this).attr('disabled', false);
        });
    }

    function get_category_name(cat_id) {
        var cat_name = '';
        switch (cat_id) {
            case 'FA':
                cat_name = 'Family';
                break;
            case 'WO':
                cat_name = 'Work';
                break;
            case 'FR':
                cat_name = 'Friends';
                break;
            case 'PE':
                cat_name = 'Personal';
                break;
            case 'OT':
                cat_name = 'Other';
        }
        return cat_name;
    }

    function get_priority_name(pri_id) {
        var pri_name = 0;
        switch (pri_id) {
            case 1:
                pri_name = '1-Highest';
                break;
            case 2:
                pri_name = '2-High';
                break;
            case 3:
                pri_name = '3-Medium';
                break;
            case 4:
                pri_name = '4-Low';
        }
        return pri_name;
    }

    function getTasks() {
        u_cancel.attr('hidden', true);
        $.ajax({
            url: 'http://127.0.0.1:8000/tasks/',
            success: function (data) {
                var target = $('#tasks-table tbody'),
                    frag = document.createDocumentFragment(),
                    newTr = null;
                target.empty();
                $(data).each(function () {
                    newTr = $('<tr/>').attr('data-id', this['id']);
                    $('<td/>').addClass('text-left').text(this['name']).appendTo(newTr);
                    $('<td/>').text(get_category_name(this['category'])).appendTo(newTr);
                    $('<td/>').text(date_helper(this['deadline'], false)).appendTo(newTr);
                    $('<td/>').addClass('text-left').text(get_priority_name(this['priority'])).appendTo(newTr);
                    $('<td/>').html(bool_helper(this['completed'])).appendTo(newTr);
                    $('<td/>').addClass('text-left').text(date_helper(this['created'], true)).appendTo(newTr);
                    $('<td/>').html('<i class="far fa-edit fa-lg"></i>').appendTo(newTr);
                    $('<td/>').html('<i class="far fa-trash-alt fa-lg"></i>').appendTo(newTr);
                    frag.append(newTr[0]);
                });
                target.append(frag);


                $('i.fa-edit').on('click', function () {
                    var id = $($(this).parents('tr')).data('id');
                    $('td.bg-info').removeClass();
                    $(this).parent().addClass('bg-info');
                    getTask(id);
                    t_id.data('id', id);
                    u_cancel.attr('hidden', false);
                });
                $('i.fa-trash-alt').on('click', function () {
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
                enable_update_form_fields();
                u_name.val(data['name']);
                u_notes.val(data['notes']);
                u_deadline.val(''); // Setting date field to empty string so it can be left empty while updating
                u_category.val(data['category']);
                u_priority.val(data['priority']);
                $(u_completed[0]).prop('checked', data['completed']);
            }
        });
    }

    function delete_task(task_id) {
        $.ajax({
            url: 'http://127.0.0.1:8000/tasks/' + task_id + '/',
            type: 'DELETE',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
            },
            success: function () {
                getTasks();
                reset_form('u_form');
                disable_update_form_fields();
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
            "completed": false
        };

        reset_form('c_form');

        if (data['name'].length > 0) {
            c_name.removeClass('field_required');
            $.ajax({
                url: 'http://127.0.0.1:8000/tasks/',
                data: data,
                type: 'POST',
                dataType: 'json',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
                },
                success: function () {
                    getTasks();
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
            "completed": u_completed[0].checked
        };

        if (data['name'].length > 0) {
            u_btn.attr('disabled', true);
            $.ajax({
                url: 'http://127.0.0.1:8000/tasks/' + t_id.data('id') + '/',
                data: data,
                type: 'PUT',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'))
                },
                success: function () {
                    getTasks();
                    reset_form('u_form');
                    disable_update_form_fields();
                    $('td.bg-info').removeClass();
                },
            });
        } else {
            u_name.addClass('field_required');
        }
    });

    c_cancel.on('click', function (e) {
        e.preventDefault();
        c_name.removeClass('field_required');
        reset_form('c_form');
    });

    u_cancel.on('click', function (e) {
        e.preventDefault();
        u_name.removeClass('field_required');
        reset_form('u_form');
        disable_update_form_fields();
        $(this).attr('hidden', true);
        $('td.bg-info').removeClass()
    });

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

    getTasks();
});