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
  console.log(req.body);

  const user = new UserModel({
    name: req.body.name,
    email: req.body.email,
    password: req.body.password,
  });

  try {
    const newUser = await user.save();
    res.status(201).json(newUser);
    console.log("User created");
  } catch (err) {
    console.log(err.message);
    res.status(400).json({ message: err.message });
  }
});

module.exports = router;
