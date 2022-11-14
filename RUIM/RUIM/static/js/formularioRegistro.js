
function removerows (tablebody) {
    var divs = tablebody.getElementsByTagName("div");
    var labels = tablebody.getElementsByTagName("label");
    while (divs.length) divs[0].parentNode.removeChild(divs[0]);
    while (labels.length) labels[0].parentNode.removeChild(labels[0]);
}

function addrows (tablebody, n) {
    for (var i=0; i<n; i++) {
        var div = document.createElement("div");
        var label = document.createElement("label");
        var span = document.createElement("span");
        var input = document.createElement("input");

        label.setAttribute("for", "id_autor"+(i+1));
        label.setAttribute("class", "requiredField");
        label.innerHTML = "Autor "+(i+1)

        span.setAttribute("class", "asteriskField text-danger");
        span.innerHTML = "*"

        input.setAttribute("type", "text");
        input.setAttribute("name", "autor"+(i+1));
        input.setAttribute("id", "id_autor"+(i+1));
        input.setAttribute("maxlength", "250");
        input.setAttribute("class", "textinput textInput form-control");
        input.setAttribute("required", "");

        div.appendChild(input);
        label.appendChild(span);
        tablebody.appendChild(label);
        tablebody.appendChild(div);
    }
}

function cambiarCampos(){
    var select = document.getElementById("id_numAutores");
    var n = select.selectedIndex+1;
    var divbody = document.getElementById("div_id_au");
    removerows(divbody);
    addrows(divbody, n);
}