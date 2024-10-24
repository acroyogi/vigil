from _localconfig import *
from _gsecrets import *
import sms_email

# active_users
# print(alert_users[active_users])

sms_email.send_alert(smtp_phonealias2, basic_alert_subject, sample_alert_message)
