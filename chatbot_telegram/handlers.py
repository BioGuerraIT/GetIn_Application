from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import ConversationHandler
import re
from sqlalchemy.exc import SQLAlchemyError
from models import User
from config import Session
from email_utils import is_valid_email
from constants import *

# Function to display available commands
async def show_commands(update: Update):
    commands = "/start - Register or view your information\n/update - Update your existing information\n/cancel - Cancel the current operation"
    await update.message.reply_text(f"Here are the functions you can use:\n{commands}")


# Define conversation handler functions
async def start(update: Update, context: CallbackContext) -> int:
    session = Session()
    user = (
        session.query(User)
        .filter(User.chat_id == str(update.effective_chat.id))
        .first()
    )
    if user:
        await update.message.reply_text(
            f"Welcome back! Here is your info:\nFirst name: {user.first_name}\nLast name: {user.last_name}\nAge: {user.age}\nSchool: {user.school}\nEmail: {user.email}\nPreferences: {user.preferences}\nBio: {user.bio}\nYou can update your information by sending /update"
        )
        Session.remove()
        return ConversationHandler.END
    else:
        await show_commands(update)  # Show available commands at the beginning
        await update.message.reply_text(
            "Hi! My name is GetIn Bot. I am here to collect some of your information in relation to our newly developed educational platform GetIn that will simplify college application experience for everyone!. First of all, what is your first name?"
        )
        return FIRST_NAME


async def first_name(update: Update, context: CallbackContext) -> int:
    context.user_data["first_name"] = (
        update.message.text.title()
    )  # Store first name with capitalization
    await update.message.reply_text("Great! Now, what is your last name?")
    return LAST_NAME


async def last_name(update: Update, context: CallbackContext) -> int:
    context.user_data["last_name"] = (
        update.message.text.title()
    )  # Store last name with capitalization
    await update.message.reply_text(
        "Nice to meet you! Can you give me your email address?"
    )
    return EMAIL


async def email(update: Update, context: CallbackContext) -> int:
    user_email = update.message.text
    if is_valid_email(user_email):
        context.user_data["email"] = user_email
        await update.message.reply_text(
            "Thank you! Now, can you tell me how old you are?"
        )
        return AGE
    else:
        await update.message.reply_text(
            "It seems like you entered an invalid email address. Please enter a valid email address."
        )
        return EMAIL


async def age(update: Update, context: CallbackContext) -> int:
    age = update.message.text
    if age.isdigit():
        context.user_data["age"] = int(age)
        await update.message.reply_text("Amazing! What school do you attend?")
        return SCHOOL
    else:
        await update.message.reply_text("Please enter a valid age.")
        return AGE


async def school(update: Update, context: CallbackContext) -> int:
    context.user_data["school"] = update.message.text
    await update.message.reply_text(
        "What are you looking for the most in GetIn?\n"
        "1. Use AI to strategize where to apply\n"
        "2. Help with SAT / ACT preparation\n"
        "3. Assistance with writing essays\n"
        "4. Affordable mentorship\n"
        "Please type the number of your choice."
    )
    return PREFERENCES


async def preferences(update: Update, context: CallbackContext) -> int:
    preference_options = {
        "1": "Use AI to strategize where to apply",
        "2": "Help with SAT / ACT preparation",
        "3": "Assistance with writing essays",
        "4": "Affordable mentorship"
    }
    
    preference_number = update.message.text
    preference_text = preference_options.get(preference_number, None)
    
    if preference_text:
        context.user_data["preferences"] = preference_text
        await update.message.reply_text(
            f"Thank you! We'll tailor our services based on your preference for: {preference_text}. Lastly, can you tell me a little about yourself?"
        )
        return BIO
    else:
        await update.message.reply_text(
            "It seems like you entered an invalid option. Please select from the following options:\n"
            "1. Use AI to strategize where to apply\n"
            "2. Help with SAT / ACT preparation\n"
            "3. Assistance with writing essays\n"
            "4. Affordable mentorship\n"
            "Please type the number of your choice."
        )
        return PREFERENCES


async def bio(update: Update, context: CallbackContext) -> int:
    session = Session()
    try:
        new_user = User(
            chat_id=str(update.effective_chat.id),
            first_name=context.user_data["first_name"],
            last_name=context.user_data["last_name"],
            age=context.user_data["age"],
            school=context.user_data["school"],
            email=context.user_data["email"],
            preferences=context.user_data["preferences"],
            bio=update.message.text,
        )
        session.add(new_user)
        session.commit()
        await update.message.reply_text(
            "Thank you for sharing about yourself, that would be all! Have a great day!"
        )
    except SQLAlchemyError as e:
        await update.message.reply_text(
            "Sorry, there was a problem saving your information. Please try again later."
        )
    finally:
        Session.remove()
    return ConversationHandler.END


async def update(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "What information would you like to update?\n1. First Name\n2. Last Name\n3. Age Name\n4. School\n5. Email\n6. Preferences\n7. Bio\nPlease choose: First Name, Last Name, Age, School, Email, Preferences, or Bio, or type /cancel to stop."
    )
    await show_commands(update)  # Show commands when update is initiated
    return UPDATE_CHOICE


async def update_choice(update: Update, context: CallbackContext) -> int:
    choice = update.message.text.lower()
    if choice in [
        "first name",
        "last name",
        "email",
        "bio",
        "age",
        "school",
        "preferences",
    ]:
        if choice == "preferences":
            await update.message.reply_text(
                "Please enter your new preferences from this list:\n"
                "What are you looking for the most in GetIn?\n"
                "1. Use AI to strategize where to apply\n"
                "2. Help with SAT / ACT preparation\n"
                "3. Assistance with writing essays\n"
                "4. Affordable mentorship\n"
                "Please type the number of your choice."
            )
        await update.message.reply_text(f"Please enter your new {choice}:")
        return {
            "first name": UPDATE_FIRST_NAME,
            "last name": UPDATE_LAST_NAME,
            "email": UPDATE_EMAIL,
            "bio": UPDATE_BIO,
            "age": UPDATE_AGE,
            "school": UPDATE_SCHOOL,
            "preferences": UPDATE_PREFERENCES,
        }[choice]
    elif choice == "done":
        await update.message.reply_text("Thank you for using our service. Goodbye!")
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "Please choose a valid option: First name, Last name, Email, Age, School, Bio, Preferences, or type Done to finish."
        )
        return UPDATE_CHOICE


async def update_first_name(update: Update, context: CallbackContext) -> int:
    new_first_name = update.message.text.title()  # Capitalize the first letter
    session = Session()
    try:
        user = (
            session.query(User)
            .filter(User.chat_id == str(update.effective_chat.id))
            .first()
        )
        if user:
            user.first_name = new_first_name
            session.commit()
            await update.message.reply_text(
                "Your first name has been updated. Would you like to update anything else? Type /update to continue or /cancel to finish."
            )
        else:
            await update.message.reply_text(
                "No user found. Please start the registration process with /start."
            )
    except SQLAlchemyError as e:
        await update.message.reply_text(
            "Sorry, there was an error updating your first name. Please try again."
        )
    finally:
        Session.remove()
    return UPDATE_CHOICE


async def update_last_name(update: Update, context: CallbackContext) -> int:
    new_last_name = update.message.text.title()  # Capitalize the first letter
    session = Session()
    try:
        user = (
            session.query(User)
            .filter(User.chat_id == str(update.effective_chat.id))
            .first()
        )
        if user:
            user.last_name = new_last_name
            session.commit()
            await update.message.reply_text(
                "Your last name has been updated. Would you like to update anything else? Type /update to continue or /cancel to finish."
            )
        else:
            await update.message.reply_text(
                "No user found. Please start the registration process with /start."
            )
    except SQLAlchemyError as e:
        await update.message.reply_text(
            "Sorry, there was an error updating your last name. Please try again."
        )
    finally:
        Session.remove()
    return UPDATE_CHOICE


async def update_email(update: Update, context: CallbackContext) -> int:
    new_email = update.message.text
    if is_valid_email(new_email):
        session = Session()
        try:
            user = (
                session.query(User)
                .filter(User.chat_id == str(update.effective_chat.id))
                .first()
            )
            user.email = new_email
            session.commit()
            await update.message.reply_text(
                "Your email has been updated. Would you like to update anything else? If not, type Done."
            )
        except SQLAlchemyError as e:
            await update.message.reply_text(
                "Sorry, there was an error updating your email."
            )
        finally:
            Session.remove()
    else:
        await update.message.reply_text(
            "You have entered an invalid email. Please enter a valid email address."
        )
        return UPDATE_EMAIL
    return UPDATE_CHOICE


async def update_age(update: Update, context: CallbackContext) -> int:
    new_age = update.message.text
    if new_age.isdigit():
        session = Session()
        try:
            user = (
                session.query(User)
                .filter(User.chat_id == str(update.effective_chat.id))
                .first()
            )
            user.age = int(new_age)
            session.commit()
            await update.message.reply_text(
                "Your age has been updated. Would you like to update anything else?"
            )
        except SQLAlchemyError as e:
            await update.message.reply_text(
                "Sorry, there was an error updating your age. Please try again."
            )
        finally:
            Session.remove()
    else:
        await update.message.reply_text("Please enter a valid age.")
        return UPDATE_AGE
    return UPDATE_CHOICE


async def update_school(update: Update, context: CallbackContext) -> int:
    new_school = update.message.text
    session = Session()
    try:
        user = (
            session.query(User)
            .filter(User.chat_id == str(update.effective_chat.id))
            .first()
        )
        user.school = new_school
        session.commit()
        await update.message.reply_text(
            "Your school has been updated. Would you like to update anything else?"
        )
    except SQLAlchemyError as e:
        await update.message.reply_text(
            "Sorry, there was an error updating your school. Please try again."
        )
    finally:
        Session.remove()
    return UPDATE_CHOICE


async def update_preferences(update: Update, context: CallbackContext) -> int:
    preference_options = {
        "1": "Use AI to strategize where to apply",
        "2": "Help with SAT / ACT preparation",
        "3": "Assistance with writing essays",
        "4": "Affordable mentorship"
    }

    preference_number = update.message.text
    new_preference_text = preference_options.get(preference_number, None)

    if new_preference_text:
        session = Session()
        try:
            user = session.query(User).filter(User.chat_id == str(update.effective_chat.id)).first()
            user.preferences = new_preference_text
            session.commit()
            await update.message.reply_text(
                f"Your preferences have been updated to: {new_preference_text}. Would you like to update anything else?"
            )
        except SQLAlchemyError as e:
            await update.message.reply_text(
                "Sorry, there was an error updating your preferences. Please try again."
            )
        finally:
            Session.remove()
        return UPDATE_CHOICE
    else:
        await update.message.reply_text(
            "It seems like you entered an invalid option. Please select from the following options:\n"
            "1. Use AI to strategize where to apply\n"
            "2. Help with SAT / ACT preparation\n"
            "3. Assistance with writing essays\n"
            "4. Affordable mentorship\n"
            "Please type the number of your choice."
        )
        return UPDATE_PREFERENCES


async def update_bio(update: Update, context: CallbackContext) -> int:
    session = Session()
    try:
        user = (
            session.query(User)
            .filter(User.chat_id == str(update.effective_chat.id))
            .first()
        )
        user.bio = update.message.text
        session.commit()
        await update.message.reply_text(
            "Your bio has been updated. Would you like to update anything else? If not, type Done."
        )
    except SQLAlchemyError as e:
        await update.message.reply_text("Sorry, there was an error updating your bio.")
    finally:
        Session.remove()
    return UPDATE_CHOICE


# Define a cancel function to allow users to stop the conversation
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Update process canceled. You can start again with /start or /update."
    )
    await show_commands(update)  # Show available commands after canceling
    return ConversationHandler.END