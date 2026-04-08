from src.app.model.account.entities.value_object import EmailStrings


email_str = EmailStrings(value="value@g")
print(email_str)
email_str.value = "test"
print(email_str)