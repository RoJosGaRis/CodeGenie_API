const mongoose = require("mongoose");

/*
### Example ###

{"user":{"name":"Roberto García","email":"a01284731@tec.mx","image":"https://avatars.githubusercontent.com/u/74624335?v=4"},"expires":"2023-10-24T00:40:44.634Z"}
*/

const UserSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true },
  password: { type: String, required: true },
});
