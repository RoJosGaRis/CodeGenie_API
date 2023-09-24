const express = require("express");
const router = express.Router();
const UserModel = require("../models/UserModel");

router.get("/users", async (req, res) => {
  try {
    const users = await UserModel.find();
    res.send(users);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// POST One
router.post("/create", async (req, res) => {
  console.log(JSON.stringify(req.body));

  const user = new UserModel({
    user: req.body.user,
    expires: req.body.expires,
  });

  try {
    const user = await user.save();
    res.status(201).json(user);
    console.log("User created");
  } catch (err) {
    console.log(err.message);
    res.status(400).json({ message: err.message });
  }
});

module.exports = router;
