function validate() {
    var username = document.forms["registrationform"]["username"].value;
    var pwd = document.forms["registrationform"]["pwd"].value;
    var fullname = document.forms["registrationform"]["fullname"].value;
    var email = document.forms["registrationform"]["email"].value;
    var telno = document.forms["registrationform"]["telno"].value;

    if (username == "" || pwd == "" || fullname == "" || email == "" || telno == "") {
        document.getElementById("hidden-paragraph").innerText = "All fields must be entered.";
        document.getElementById("hidden-paragraph").style.display = "block";
        return false;
    }

    document.getElementById("hidden-paragraph").innerText = "";
    document.getElementById("hidden-paragraph").style.display = "none";
    return true;
}
