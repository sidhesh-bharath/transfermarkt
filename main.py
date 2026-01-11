import auth
import db

user, session = auth.sign_up_user("sidheshbharath21@gmail.com", "Sidhesh@2011")
db.update_user("Sidhesh", 10000, ["Cristiano Ronaldo", "Lionel Messi"])