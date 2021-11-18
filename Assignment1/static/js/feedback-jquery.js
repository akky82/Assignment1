$(document).ready(function() {
    $("feedback").submit(function(e){
        if (ValidateFeedback())
        {
            return true;
        }
        else
        {
            e.preventDefault();
            return false;
        }
    });
});