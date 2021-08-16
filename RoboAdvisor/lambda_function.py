### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta

### Functionality Helper Functions ###
def parse_val(n,to_type):
    """
    Securely converts string value to integer or float.
    """
    # Test for the type, then convert
    # else return NaN
    if isinstance(n,str) and to_type == 'int':
        try:
            # convert the string to float before int
            # to provide the best chance of success
            return int(float(n))
        except ValueError:
            return float("NaN")
    elif isinstance(n,str) and to_type == 'float':
        try:
            return float(n)
        except ValueError:
            # In the event that investment amount is not able to be
            # converted to a float, then return 0 which will force
            # another prompt for the correct value as opposed to
            # accepting and "working around" an incorrect value
            return float("0")


def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


def validate_data(age, investment_amount, intent_request):
    """
    Validates the data provided by the user.
    """

    # Validate that the user:
    #  - has been born!
    #  - is less than the age of 65
    if age is not None:   # if not null, validate
        # Parameters coming through from the Bot (AWS Lex)
        # will be strings, so it is important to cast them to float
        age = parse_val(age,'int')
        if age < 0 or age > 64:
            return build_validation_result(
                False,
                "age",
                "The maximum age to contract this service is 64, can you provide an age between 0 and 64 please?",
            )

    # Validate that investment_amount is > 0
    if investment_amount is not None:  # if not null, validate
        # Parameters coming through from the Bot (AWS Lex)
        # will be strings, so it is important to cast them to float
        #
        # For this particular function, validating investment_amount
        # is not required to provide a result back to the user
        # but I'm doing it anyway :)
        investment_amount = parse_val(investment_amount,'float')
        if investment_amount < 5000 or not isinstance(investment_amount,float):
            return build_validation_result(
                False,
                "investmentAmount",
                "The minimum investment amount is $5,000 USD, could you please provide a greater amount?",
            )

    # A True result is returned if age or investment_amount are valid
    return build_validation_result(True, None, None)


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response


### Intents Handlers ###
def recommend_portfolio(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    # Get specific values for slot names
    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investment_amount = get_slots(intent_request)["investmentAmount"]
    risk_level = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.

        # Gets all the slots for processing later
        slots = get_slots(intent_request)

        # Validates user's input using validate_data()
        validation_result = validate_data(age, investment_amount, intent_request)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )

        # Fetch current session attibutes
        output_session_attributes = intent_request["sessionAttributes"]

        return delegate(output_session_attributes, get_slots(intent_request))

    ### If the data provided is valid, then set
    #   the appropriate recommendation

    # Make sure we're working with predictable values
    risk_level = risk_level.lower()

    # Determine the recommendation based on risk level
    if risk_level == 'none' or risk_level == 'zero':
        initial_recommendation = "100% bonds (AGG), 0% equities (SPY)"

    elif risk_level == 'very low':
        initial_recommendation = "80% bonds (AGG), 20% equities (SPY)"

    elif risk_level == 'low':
        initial_recommendation = "60% bonds (AGG), 40% equities (SPY)"

    elif risk_level == 'medium':
        initial_recommendation = "40% bonds (AGG), 60% equities (SPY)"

    elif risk_level == 'high':
        initial_recommendation = "20% bonds (AGG), 80% equities (SPY)"

    elif risk_level == 'very high':
        initial_recommendation = "0% bonds (AGG), 100% equities (SPY)"

    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{} thank you for your information;
            based on the risk level you defined, my recommendation is to choose an investment portfolio with {}
            """.format(
                first_name, initial_recommendation
            ),
        },
    )


### Intents Dispatcher ###
def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    # Get the name of the current intent
    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "RecommendPortfolio":
        return recommend_portfolio(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)
