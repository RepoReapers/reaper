// JavaScript function to get status of a HTTP GET request using XHR
function getStatus(url) {
    var request = new XMLHttpRequest();
    request.open("GET", url, true);
    request.send();

    request.onreadystatechange = function() {
        if (request.readyState == 4) {
            return(request.responseText);
        }
    }
}
