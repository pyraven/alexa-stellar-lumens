# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the implementation of handler classes approach in skill builder.

import logging
import os
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

import requests
from stellar_base.builder import Builder

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

secret = os.environ["SECRET"]
wallet = os.environ["WALLET"] 
friend_one = os.environ["FRIENDONE"]
friend_two = os.environ["FRIENDTWO"]
address_book = {"nicholas": friend_one, "timothy": friend_two}

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Hello World", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = (
            "The Hello World skill can't help you with that.  "
            "You can say hello!!")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)
        speech = "Sorry, there was some problem. Please try again."
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response

##################################
#### Custom Skills w/ Stellar ####
##################################

class PriceReportIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PriceReportIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        data = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd").json()
        current_price = ''.join(str(i['current_price']) for i in data if i['id'] == 'stellar')
        price_high = ''.join(str(i['high_24h']) for i in data if i['id'] == 'stellar')
        alexa_price = round(float(current_price), 4)
        alexa_price_high = round(float(price_high), 4)
        speech_text = f'The current price of stellar is {alexa_price} cents with a 24-hour high of {alexa_price_high} cents.'
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class NetWorthIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("NetWorthIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        bank = "https://horizon-testnet.stellar.org/accounts/" + wallet
        balances = requests.get(bank).json()['balances']
        amount = float(''.join(i['balance'] for i in balances))
        data = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd").json()
        current_price = ''.join(str(i['current_price']) for i in data if i['id'] == 'stellar')
        alexa_price = float(current_price)
        net_worth = round(alexa_price * amount, 2)
        speech_text = f'Your net worth is {net_worth} dollars.'
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class LamboCheckHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("LamboCheckIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        bank = "https://horizon-testnet.stellar.org/accounts/" + wallet
        balances = requests.get(bank).json()['balances']
        amount = float(''.join(i['balance'] for i in balances))
        data = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd").json()
        current_price = ''.join(str(i['current_price']) for i in data if i['id'] == 'stellar')
        alexa_price = float(current_price)
        net_worth = round(alexa_price * amount, 2)
        lambo = 200000.00
        if net_worth < lambo:
            diff_in_price = round(lambo - net_worth, 2)
            speech_text = f'You are short {diff_in_price} dollars before you can afford a lamborghini.'
        else:
            speech_text = 'Come pick me up.'
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response

class CheckBalanceIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("CheckBalanceIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        bank = "https://horizon-testnet.stellar.org/accounts/" + wallet
        balances = requests.get(bank).json()['balances']
        amount = float(''.join(i['balance'] for i in balances))
        total = round(amount, 2)
        speech_text = f'You have a balance of {total} stellar in your account.'
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(False)
        return handler_input.response_builder.response


class SendStellarIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SendStellarIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = ""
        slots = handler_input.request_envelope.request.intent.slots
        stellar = slots["amount"].value
        receiver = slots["contact"].value
        if receiver.lower() in address_book:
            account = ''.join(value for key, value in address_book.items() if receiver.lower() == key.lower())
            builder = Builder(secret=secret)
            builder.append_payment_op(destination=account, amount=stellar, asset_code='XLM')
            builder.sign()
            response = builder.submit()
            speech_text = f"{stellar} stellar has been sent to {receiver}."
        else:
            speech_text = "I could not find that contact in your address book."
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response

# default handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# custom request handler
sb.add_request_handler(PriceReportIntentHandler())
sb.add_request_handler(NetWorthIntentHandler())
sb.add_request_handler(LamboCheckHandler())
sb.add_request_handler(CheckBalanceIntentHandler())
sb.add_request_handler(SendStellarIntentHandler())

# exception handler
sb.add_exception_handler(CatchAllExceptionHandler())

# build the handler
handler = sb.lambda_handler()