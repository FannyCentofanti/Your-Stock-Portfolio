{
    // Load google charts
    google.charts.load('current', { 'packages': ['corechart'] });

    // draw the pie charts when the page is loaded.
    $(document).ready(function () {

        if (location.pathname == '/') {
            var display_data = JSON.parse(document.getElementById("display_table").dataset.display);
            var total_value_display = JSON.parse(document.getElementById("display_table").dataset.displayvalue);

            google.charts.setOnLoadCallback(function () {
                drawChart_start(display_data, total_value_display);
            });
        }
        else if (location.pathname == '/getstarted/') {
            var display_data = JSON.parse(document.getElementById("display_table").dataset.display);
            var total_value_display = JSON.parse(document.getElementById("display_table").dataset.displayvalue);

            google.charts.setOnLoadCallback(function () {
                drawChart_getstarted(display_data, total_value_display);
            });
        }
        else if (location.pathname == '/userhome/') {

            var my_modal = document.getElementById('my_modal');

            var user_data = JSON.parse(document.getElementById("user_table").dataset.user);
            var total_value = JSON.parse(document.getElementById("user_table").dataset.value);

            google.charts.setOnLoadCallback(function () {
                drawChart_userhome(user_data, total_value);
            });

            // listen to event for Add/Remove button in table.
            // display modal to ask for edit of amount of shares.
            my_modal.addEventListener('show.bs.modal', function (event) {
                // Button that triggered the modal
                var button = event.relatedTarget;
                // Extract info from data-bs-* attributes
                var symbol = button.getAttribute('data-bs-symbol');
                var action = button.getAttribute('data-bs-action');
                // Update the modal's content.
                var modalTitle = my_modal.querySelector('#action');
                var modalBody = my_modal.querySelector('#symbol');

                modalTitle.textContent = action + ' shares';
                modalBody.textContent = 'For company with symbol: ' + symbol;

                // update title attribute
                $('#action').attr('title', action);
                $('#symbol').attr('title', symbol);
            })
            
        }
    });

    // redraw the charts if the size of the window changes.
    $(window).resize(function () {

        if (location.pathname == '/') {
            var display_data = JSON.parse(document.getElementById("display_table").dataset.display);
            var total_value_display = JSON.parse(document.getElementById("display_table").dataset.displayvalue);

            google.charts.setOnLoadCallback(function () {
                drawChart_start(display_data, total_value_display);
            });
        }
        else if (location.pathname == '/getstarted/') {
            var display_data = JSON.parse(document.getElementById("display_table").dataset.display);
            var total_value_display = JSON.parse(document.getElementById("display_table").dataset.displayvalue);

            google.charts.setOnLoadCallback(function () {
                drawChart_getstarted(display_data, total_value_display);
            });
        }
        else if (location.pathname == '/userhome/') {
            var user_data = JSON.parse(document.getElementById("user_table").dataset.user);
            var total_value = JSON.parse(document.getElementById("user_table").dataset.value);

            google.charts.setOnLoadCallback(function () {
                drawChart_userhome(user_data, total_value);
            });
        }
    });

    // Draw the chart and set the chart values for start page
    function drawChart_start(display_data, total_value_display) {
        var chart_data = get_chart_data(display_data, total_value_display);
        var data = google.visualization.arrayToDataTable(chart_data);

        // Optional; add a title and set the width and height of the chart
        var options = {
            title: 'The distribution of your stock portfolio',
            titleTextStyle: { color: '#212529', fontSize: '22', bold: 'False', fontName: 'Helvetica' },
            chartArea: { 'width': '80%', 'height': '92%', 'top': '36', 'right': '30', 'bottom': '30', 'left': '30' },
            legend: { 'position': 'right', 'alignment': 'center' },
            colors: ['#F94144', '#F3722C', '#F8961E', '#F9844A', '#F9C74F', '#90BE6D', '#43AA8B', '#4D908E', '#577590', '#277DA1']
        };

        // Display the chart inside the <div> element with id="piechart"
        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);
    }


    // Draw the chart and set the chart values
    function drawChart_getstarted(display_data, total_value_display) {
        var chart_data = get_chart_data(display_data, total_value_display);
        var data = google.visualization.arrayToDataTable(chart_data);

        // Optional; add a title and set the width and height of the chart
        var options = {
            title: 'The distribution of your stock portfolio',
            titleTextStyle: { color: '#212529', fontSize: '18', bold: 'False', fontName: 'Helvetica' },
            chartArea: { 'width': '80%', 'height': '92%', 'top': '36', 'right': '30', 'bottom': '30', 'left': '30' },
            legend: { 'position': 'right', 'alignment': 'center' },
            colors: ['#F94144', '#F3722C', '#F8961E', '#F9844A', '#F9C74F', '#90BE6D', '#43AA8B', '#4D908E', '#577590', '#277DA1']
        };

        // Display the chart inside the <div> element with id="getstarted-piechart"
        var chart = new google.visualization.PieChart(document.getElementById('getstarted-piechart'));
        chart.draw(data, options);
    }

    // Draw the chart and set the chart values for start page
    function drawChart_userhome(user_data, total_value) {
        var chart_data = get_chart_data(user_data, total_value);
        if (chart_data == -1) {
            drawPiechartblank();
            return;
        }
        var data = google.visualization.arrayToDataTable(chart_data);

        // Optional; add a title and set the width and height of the chart
        var options = {
            title: 'The distribution of your stock portfolio',
            titleTextStyle: { color: '#212529', fontSize: '22', bold: 'False', fontName: 'Helvetica' },
            chartArea: { 'width': '80%', 'height': '92%', 'top': '36', 'right': '30', 'bottom': '30', 'left': '30' },
            legend: { 'position': 'right', 'alignment': 'center' },
            colors: ['#F94144', '#F3722C', '#F8961E', '#F9844A', '#F9C74F', '#90BE6D', '#43AA8B', '#4D908E', '#577590', '#277DA1']
        };

        // Display the chart inside the <div> element with id="piechart"
        var chart = new google.visualization.PieChart(document.getElementById('piechart'));
        chart.draw(data, options);
    }

    // draw empty pie chart.
    // With help from answer from WhiteHat: 
    // https://stackoverflow.com/questions/42695645/java-script-google-pie-chart-show-an-empty-pie-chart-if-there-is-no-data-to-sho
    function drawPiechartblank() {
        var data = google.visualization.arrayToDataTable([
            ['Industry', 'Procent'],
          // blank first column removes legend,
          // use object notation for formatted value (f:)
          ['', {v: 1, f: 'No Data'}]
        ]);
      
        var options = {
            title: 'The distribution of your stock portfolio',
            titleTextStyle: { color: '#212529', fontSize: '22', bold: 'False', fontName: 'Helvetica' },
            chartArea: { 'width': '80%', 'height': '92%', 'top': '36', 'right': '30', 'bottom': '30', 'left': '30' },
            legend: { 'position': 'right', 'alignment': 'center' },
            colors: ['#F94144', '#F3722C', '#F8961E', '#F9844A', '#F9C74F', '#90BE6D', '#43AA8B', '#4D908E', '#577590', '#277DA1']
        };
        
        // Display the chart inside the <div> element with id="piechart"
        var chart = new google.visualization.PieChart(
          document.getElementById('piechart')
        );
        chart.draw(data, options);
    }

    // create the data to draw the pie chart.
    function get_chart_data(user_portfolio, total_value) {

        // varible decleration.
        var data = user_portfolio;
        var total_value = total_value;

        // get the length of the table to check if there is any data to draw in chart.
        var table_length;
        if (document.getElementById("user_data_table").rows.length == 1) {
            return -1;
        }
        else {
            table_length = document.getElementById("user_data_table").rows.length;
        }

        // get the ground for the data to draw the pie chart.
        var request = new XMLHttpRequest();
        request.open("GET", "/static/diagram_data_structure.json", false);
        request.send(null)
        var json_data = JSON.parse(request.responseText);

        // create a new array.
        var data_array = new Array(json_data.sectors.length);
        data_array[0] = ['Industry', 'Procent'];

        // assigning total value of all sectors in the user portfolio.
        for (let i = 0; i < (table_length - 1); i++) {
            for (let j = 0; j < json_data.sectors.length; j++) {
                if (data[i].sector == json_data.sectors[j].name) {
                    if (data[i].total_value == "NaN") {
                        continue;
                    }
                    json_data.sectors[j].percent += data[i].total_value;
                }
            }
        }

        // dividing the value of all sectors with the total value of the portfolio
        // to get the prercent of each sector.
        for (let k = 1; k < json_data.sectors.length; k++) {
            var value_percent = (
                json_data.sectors[k].percent / total_value);
            data_array[k] = [json_data.sectors[k].name, value_percent];
        }

        return data_array;
    }

    // handle change in user portfolio from form and Add/Remove button.
    function data_handler(event) {

        if (event == "new_company") {
            var shares = $('#shares_input').val().trim();
            if (shares < 0) shares *= -1;
            var symbol = $('#symbol_input').val().trim();
            symbol = symbol.toUpperCase();
            var url = '/userhome/new-company/';
            var js_object = { "symbol": symbol, "shares": shares };
            ajax_request(url, js_object);
            
            // empting the input in the form.
            var symbol_input = document.getElementById("symbol_input");
            symbol_input.value = '';
            var shares_input = document.getElementById("shares_input");
            shares_input.value = '';

        }
        else if (event == "edit_share") {
            var shares = $('#share_edit_input').val().trim();
            if (shares < 0) shares *= -1;
            var action = $('#action').attr('title');
            var symbol = $('#symbol').attr('title');
            symbol = symbol.toUpperCase();
            var url = '/userhome/edit_shares/';
            var js_object = { "action": action, "symbol": symbol, "shares": shares };
            ajax_request(url, js_object);
            
            // empting the input in the form.
            var modal_shares_input = document.getElementById("share_edit_input");
            modal_shares_input.value = '';

        }
        else {
            alert("Something went wrong, try again.");
        }
    }

    // ajax request for change in user portfolio.
    function ajax_request(url, js_object) {

        $.ajax({
            url: url,
            data: JSON.stringify(js_object),
            contentType: 'application/json',
            type: 'POST',
            success: function (response) {
                console.log(response);
                response_handler(response);
            },
            error: function (error) {
                console.log(error);
                // alert(error.responseText);
                error_handler("AJAX", error);
            }
        });
    }

    // response handler to handle the respons from the AJAX-request.
    function response_handler(response) {

        // get the json-data in the response.
        var data = JSON.parse(response);

        // error handling if user data is empty.
        if (data.user_data.length == 0 && data.nr_companies > 0) {
            var responseText = "Something went wrong. Please try again.";
            error_handler("function", responseText);
            return;
        }

        // get the table to be able to modify it.
        var user_data_table = document.getElementById("user_data_table");

        // the event in data tells how the reponse should be handeled.
        // if event is edit, shares has been edited to a company current in the user portfolio,
        // thus the size of the table dosen't need to be adjusted. The table is drawn with
        // the new data.
        if (data.event == "edit") {
            for (var i = 1, row; row = user_data_table.rows[i]; i++) {

                user_data_table.rows[i].cells[0].innerHTML = data.user_data[i - 1].symbol;
                user_data_table.rows[i].cells[1].innerHTML = data.user_data[i - 1].company_name;
                user_data_table.rows[i].cells[2].innerHTML = data.user_data[i - 1].shares;
                user_data_table.rows[i].cells[3].innerHTML = data.user_data[i - 1].current_stock_value;
                user_data_table.rows[i].cells[4].innerHTML = data.user_data[i - 1].total_value;
                user_data_table.rows[i].cells[5].innerHTML = data.user_data[i - 1].industry;
                user_data_table.rows[i].cells[6].innerHTML = data.user_data[i - 1].sector;
                user_data_table.rows[i].cells[7].innerHTML = "<button class='btn btn-success' type='button' data-bs-toggle='modal'" +
                    "data-bs-target='#my_modal' data-bs-symbol='" + data.user_data[i - 1].symbol + "' data-bs-action='Add'>Add</button>";
                user_data_table.rows[i].cells[8].innerHTML = "<button class='btn btn-danger' type='button' data-bs-toggle='modal' " +
                    "data-bs-target='#my_modal' data-bs-symbol='" + data.user_data[i - 1].symbol + "' data-bs-action='Remove'>Remove</button></td>";
            }
        }
        // if event is new, a new company is added to the user portfolio,
        // thus a row is added to the table and the table is drawn with the new data.
        else if (data.event == "new") {

            // append a row to the tabel.
            append_table_row();

            for (var i = 1, row; row = user_data_table.rows[i]; i++) {

                user_data_table.rows[i].cells[0].innerHTML = data.user_data[i - 1].symbol;
                user_data_table.rows[i].cells[1].innerHTML = data.user_data[i - 1].company_name;
                user_data_table.rows[i].cells[2].innerHTML = data.user_data[i - 1].shares;
                user_data_table.rows[i].cells[3].innerHTML = data.user_data[i - 1].current_stock_value;
                user_data_table.rows[i].cells[4].innerHTML = data.user_data[i - 1].total_value;
                user_data_table.rows[i].cells[5].innerHTML = data.user_data[i - 1].industry;
                user_data_table.rows[i].cells[6].innerHTML = data.user_data[i - 1].sector;
                user_data_table.rows[i].cells[7].innerHTML = "<button class='btn btn-success' type='button' data-bs-toggle='modal'" +
                    "data-bs-target='#my_modal' data-bs-symbol='" + data.user_data[i - 1].symbol + "' data-bs-action='Add'>Add</button>";
                user_data_table.rows[i].cells[8].innerHTML = "<button class='btn btn-danger' type='button' data-bs-toggle='modal' " +
                    "data-bs-target='#my_modal' data-bs-symbol='" + data.user_data[i - 1].symbol + "' data-bs-action='Remove'>Remove</button></td>";
            }
        }
        // if event is remove, shares has been removed to a company current in the user portfolio
        // and the shares of the company is zero. The table is drawn with the new data.
        else if (data.event == "remove")
        {
            // remove a row in table.
            delete_table_row();

            for (var i = 1, row; row = user_data_table.rows[i]; i++) {

                user_data_table.rows[i].cells[0].innerHTML = data.user_data[i - 1].symbol;
                user_data_table.rows[i].cells[1].innerHTML = data.user_data[i - 1].company_name;
                user_data_table.rows[i].cells[2].innerHTML = data.user_data[i - 1].shares;
                user_data_table.rows[i].cells[3].innerHTML = data.user_data[i - 1].current_stock_value;
                user_data_table.rows[i].cells[4].innerHTML = data.user_data[i - 1].total_value;
                user_data_table.rows[i].cells[5].innerHTML = data.user_data[i - 1].industry;
                user_data_table.rows[i].cells[6].innerHTML = data.user_data[i - 1].sector;
                user_data_table.rows[i].cells[7].innerHTML = "<button class='btn btn-success' type='button' data-bs-toggle='modal'" +
                    "data-bs-target='#my_modal' data-bs-symbol='" + data.user_data[i - 1].symbol + "' data-bs-action='Add'>Add</button>";
                user_data_table.rows[i].cells[8].innerHTML = "<button class='btn btn-danger' type='button' data-bs-toggle='modal' " +
                    "data-bs-target='#my_modal' data-bs-symbol='" + data.user_data[i - 1].symbol + "' data-bs-action='Remove'>Remove</button></td>";
            }
        }

        // draw the pie chart with the modified data.
        google.charts.setOnLoadCallback(function () {
            drawChart_userhome(data.user_data, data.total_value_holdnings);
        });
    }

    // error handling from AJAX-request and if user data is empty.
    function error_handler(info_error, response) {
        
        if (info_error == "AJAX") {
            // get the json-data in the response.
            var error = JSON.parse(response.responseText);
            alert(error.message);
        }
        else if (info_error == "function") {
            alert(response);
        }
        else {
            alert("Unidentified error");
        }    
    }

    // function to add row in table.
    function append_table_row() {

        var table = document.getElementById("user_data_table");

        var row = table.insertRow(table.rows.length);

        for (i = 0; i < table.rows[0].cells.length; i++) {
            add_table_cell(row.insertCell(i));
        }
    }
    // function to add cell in table.
    function add_table_cell(cell) {

        var div = document.createElement('div');
        cell.appendChild(div);
    }

    // function to delete the last row in table.
    function delete_table_row() {

        var table = document.getElementById("user_data_table");

        nr_rows = table.rows.length;

        table.deleteRow(nr_rows-1);
    }
    
}