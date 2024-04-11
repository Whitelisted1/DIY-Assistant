import helpful_assistant


def init(app: helpful_assistant.Assistant):
    module = helpful_assistant.Module("Weather", "Get information relating to the weather")
    helpful_assistant.Action("Cloud_Conditions", "Get the current conditions of the clouds", lambda: "Cloudy", module)
    helpful_assistant.Action("Air_Temperature", "Get the current air temperature", lambda: "80 Degrees F", module)
    helpful_assistant.Action("Wind_Speed", "Get the current wind speed", lambda: "5 MPH NW", module)

    app.add_module(module)

    module = helpful_assistant.Module("Location", "Gets information relating to locations")
    helpful_assistant.Action("Current_Location", "Get the current location of the user", lambda: "Orlando, Florida", module)

    app.add_module(module)
