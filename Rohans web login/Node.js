const express = require("express");
const fs = require("fs");
const app = express();

app.use(express.urlencoded({ extended: true }));

const USERS_FILE = "users.txt";

// SIGNUP
app.post("/signup", (req, res) => {
    const { name, email, password } = req.body;

    const entry = `${email}|${password}|${name}\n`;

    fs.appendFileSync(USERS_FILE, entry);

    res.send("Account created! <a href='/login.html'>Login</a>");
});

// LOGIN
app.post("/login", (req, res) => {
    const { email, password } = req.body;

    if (!fs.existsSync(USERS_FILE)) {
        return res.send("No users registered yet.");
    }

    const users = fs.readFileSync(USERS_FILE, "utf8").trim().split("\n");

    for (const user of users) {
        const [savedEmail, savedPassword, savedName] = user.split("|");

        if (email === savedEmail && password === savedPassword) {
            return res.send(`Welcome back, ${savedName}!`);
        }
    }

    res.send("Invalid login. <a href='/login.html'>Try again</a>");
});

// START SERVER
app.listen(3000, () => {
    console.log("Server running on http://localhost:3000");
});


