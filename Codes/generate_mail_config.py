
import configparser

config_file = configparser.ConfigParser()
config_file.add_section("SMTPlogin")

# Add settings to section
# Here you need to modify the values of last parameter of set function
sender = input("Enter email address of sender: ")
receiver = input("Enter email address of receiver: ")
config_file.set("SMTPlogin", "sender_address", sender)
config_file.set("SMTPlogin", "receiver_address", receiver)
config_file.set("SMTPlogin", "mailtrap_user", "8893a2ba101d5f")
config_file.set("SMTPlogin", "mailtrap_password", "1d160f6226faa1")

# Saving config file as configurations.ini
with open(r"configurations.ini", 'w') as configfileObj:
    config_file.write(configfileObj)
    configfileObj.flush()
    configfileObj.close()

print("Config file 'configurations.ini' created")
