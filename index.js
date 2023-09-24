require("dotenv").config();

const mongoose = require("mongoose");
const express = require("express");
const cors = require("cors");
const app = express();
const port = 4000;

app.use(
  cors({
    origin: "http://localhost:3000",
    methods: "GET,HEAD,PUT,PATCH,POST,DELETE",
    credentials: true,
  })
);
mongoose.connect(process.env.DATABASE_URL, { useNewUrlParser: true });

const db = mongoose.connection;

db.on("error", (error) => console.error(error));
db.once("open", () => {
  console.log("Connected to MongoDB");
});

app.use(express.json());

app.get("/", (req, res) => {
  res.send(res.json({ value: "Hello World!" }));
});

const usersRouter = require("./routes/users");
app.use("/users", usersRouter);

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
