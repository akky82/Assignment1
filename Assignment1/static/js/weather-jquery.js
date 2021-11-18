$(document).ready(function() {
    $("weather").submit(function(e){
        if (ValidateWeather())
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