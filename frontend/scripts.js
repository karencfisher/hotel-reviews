function loadDoc(route, method, target) {
    const apiURL = 'http://localhost:5000/api/v1.0/' + route;
    var xhttpRequest = new XMLHttpRequest();

    xhttpRequest.onerror = function() {
        alert('An error has occured. Possibly the service is unavailable.')
    }

    xhttpRequest.onload = function() { 
        if (xhttpRequest.status !== 200){
            alert('Request for ' + target + ' returned ' + xhttpRequest.status);
            return;
        }

        var ob = document.getElementById(target);
        if (ob.nodeName == "DIV") {
            document.getElementById(target).innerHTML = this.responseText;
        }
        else if (ob.nodeName == "TABLE") {
            updateTable(ob, this.responseText);
        }
        else {
            alert(ob.nodeName + ': We dont know what to do here');
        }
    }

    xhttpRequest.open(method, apiURL, true);
    xhttpRequest.send();
}

function submitForm(formData, target) {
    var xhttpRequest = new XMLHttpRequest();

    xhttpRequest.onerror = function() {
        alert('An error occur. Possibly service is unavailable.')
    }

    xhttpRequest.onload = function() { 
        alert(this.responseText);
    }

    xhttpRequest.open(formData.method, formData.action, true);
    xhttpRequest.send(new FormData(formData)); 
}

function updateTable(table_obj, contents) {
    // get column names
    var col_names = [];
    var num_cols = table_obj.rows[0].cells.length;
    for (let i = 0; i < num_cols; i++) {
        col_names.push(table_obj.rows[0].cells[i].innerHTML);
    }

    // delete rows (if any)
    for (let i = 1; i < table_obj.rows.length; i++) {
        table_id.deleteRow(i);
    }
    
    // insert rows
    var json_obj = JSON.parse(contents);
    var num_objs = json_obj.length;
    for (let i = 0; i < num_objs; i++) {
        var row = table_obj.insertRow(i + 1);
        for (let j = 0; j < num_cols; j++) {
            var cell = row.insertCell(j);
            cell.innerHTML = json_obj[i][col_names[j]];
        }
    }
}