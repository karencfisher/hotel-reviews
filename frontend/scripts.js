function loadDoc(route, method, target) {
    const apiURL = 'http://localhost:5000/api/v1.0/' + route;
    var xhttpRequest = new XMLHttpRequest();
    xhttpRequest.onload = function() { 
        document.getElementById(target).innerHTML = this.responseText;
    }
    xhttpRequest.open(method, apiURL, true);
    xhttpRequest.send();
}

function submitForm(formData) {
    var xhttpRequest = new XMLHttpRequest();
    xhttpRequest.onload = function() { 
        alert(this.responseText);
        if (xhttpRequest.status === 200) {
            loadDoc('setup/get_topics', 'GET', 'demo');
        }
    }
    xhttpRequest.open(formData.method, formData.action, true);
    xhttpRequest.send(new FormData(formData)); 
}