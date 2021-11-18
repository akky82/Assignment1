// Use regex to validate format of the email
function ValidateEmail(email)
{
    var mailFormat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (email.value.match(mailFormat))
    {
        return true;
    }
    else
    {
        alert("Please enter a valid email address!");
        document.feedback.email.focus();
        return false;
    }
}

/* Validate the form, seperate function from ValidateEmail for the ability to
add validation for more fields later if required */
function ValidateFeedback()
{
    var email = document.feedback.email;

    if (ValidateEmail(email))
    {
        return true;
    }
    else
    {
        return false;
    }
}

// Use regex to validate the format of the co-ordinates
function ValidateCoord(coord, latlong)
{
    var decimal = /^[-+]?[0-9]+\.[0-9]+$/;
    var numbers = /^[0-9]+$/;

    if (coord.value.match(decimal) || coord.value.match(numbers))
    {
        return true;
    }
    else
    {
        if (latlong == 0)
        {
            alert('Please enter a valid Latitude.');
            document.weather.latitude.focus();
            return false;
        }
        else
        {
            alert('Please enter a valid Longitude.');
            document.weather.longitude.focus();
            return false;
        }
    }
}

/* Validate the form, seperate function from ValidateCoord for the ability to
add validation for more fields later if required */
function ValidateWeather()
{
    var lat = document.weather.latitude;
    var long = document.weather.longitude;

    if (ValidateCoord(lat, 0) && ValidateCoord(long, 1))
    {
        return true;
    }
    else
    {
        return false;
    }
}