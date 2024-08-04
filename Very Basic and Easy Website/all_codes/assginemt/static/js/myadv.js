function validate() {
            var title = document.forms["advertisementform"]["title"].value
            var desc = document.forms["advertisementform"]["desc"].value

            if (title == "") {
                document.getElementById("advertisement_error").innerText = "Title must be entered."
                document.getElementById("advertisement_error").style.display = "block";
                return false;
            }
            if (desc == "") {
                document.getElementById("advertisement_error").innerText = "Description must be entered."
                document.getElementById("advertisement_error").style.display = "block";
                return false;
            }

            document.getElementById("advertisement_error").innerText = "";
            document.getElementById("advertisement_error").style.display = "none";
            return true;
        }