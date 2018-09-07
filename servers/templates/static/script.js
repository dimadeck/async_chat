    $(function() {
        var conn = null;
        var login_status = false;
        var send_mode = null;
        update_ui();
        $('#field_name').val('').focus();

        function log(msg) {
            var control = $('#log');
            control.html(control.html() + msg + '<br/>');
            control.scrollTop(control.scrollTop() + 1000);
        }

        function set_send_mode() {
            var list = document.getElementById("user_list");
            index = list.options.selectedIndex;
            if (index == -1) {
                index = 0;
            }
            if (index >= 0) {
                option = list.options[index];
                send_mode = option.value;
                $('#target').text(option.text);
                $('#text').focus();
            }
        }

        function connect() {
            disconnect();
            var wsUri = (window.location.protocol == 'https:' && 'wss://' || 'ws://') + window.location.host + '/ws';
            conn = new WebSocket(wsUri);
            var name = $('#field_name').val();
            login_status = false;
            conn.onopen = function() {
                conn.send('login ' + name);
                update_ui();
            };
            conn.onmessage = function(e) {
                var data = JSON.parse(e.data);
                switch (data.action) {
                    case 'response':
                        log(data.message);
                        if (login_status == false) {
                            if (data.message.indexOf('login to chat') > 0) {
                                login_status = true;
                            }
                        }
                        if (login_status == true) {
                            conn.send('/userlist');
                            update_ui();
                        }
                        break;
                    case 'list':
                        $('#user_list').empty();
                        $('#user_list').append($('<option>', {
                            value: 'msgall ',
                            text: 'All'
                        }));
                        $('#user_list').append($('<option>', {
                            value: '',
                            text: 'Clear data'
                        }));
                        for (i in data.message) {
                            $('#user_list').append($('<option>', {
                                value: 'msg ' + data.message[i] + ' ',
                                text: data.message[i]
                            }));
                        }
                        if (send_mode == null) {
                            set_send_mode();
                        }
                        break;
                }
            };
            conn.onclose = function() {
                log('Disconnected.');
                conn = null;
                login_status = false;
                update_ui();
            };
        }

        function disconnect() {
            if (login_status == true) {
                conn.send('logout');
                update_ui();
            }
        }

        function update_ui() {
            if (login_status == false) {
                $('#chat_viewport').prop("hidden", true);
                document.getElementById('log').innerHTML = '';
                $('#status').prop("src", '/static/images/ofline.png');
                $('#connect').prop("src", '/static/images/login.png');
                $('#send').prop("disabled", true);
                $('#name').prop("hidden", true);
                $('#field_name').prop("hidden", false);
                $('#field_name').val(name).focus();
            } else {
                $('#chat_viewport').prop("hidden", false);
                $('#status').prop("src", '/static/images/online.png');
                $('#connect').prop("src", '/static/images/logout.png');
                $('#send').prop("disabled", false);
                $('#name').prop("hidden", false);
                $('#field_name').prop("hidden", true);
                $('#text').val('').focus();
            }
            $('#name').text(name);
        };
        $('#connect').on('click', function() {
            if (conn == null) {
                connect();
            } else {
                disconnect();
            }
            if (login_status == false) {
                name = $('#field_name').val();
                conn.send('login ' + name);
            }
            update_ui();
            return false;
        });
        $('#field_name').on('keyup', function(e) {
            if (e.keyCode === 13) {
                $('#connect').click();
                return false;
            }
        });
        // Login end
        // Send start
        $('#send').on('click', function() {
            var text = $('#text').val();
            conn.send(send_mode + text);
            $('#text').val('').focus();
            return false;
        });
        $('#text').on('keydown', function(e) {
            if (e.keyCode === 13) {
                e.preventDefault();
                whenEnterPressed();
            }
        });
        $('#text').on('keyup', function(e) {
            if (e.keyCode === 13) {
                $('#send').click();
                return false;
            }
        });
        // Send end
        $('#user_list').on('dblclick', function() {
            set_send_mode();
            return false;
        });
    });
