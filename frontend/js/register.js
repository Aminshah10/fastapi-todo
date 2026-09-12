const registerForm = document.getElementById("register-form");

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    const userData = {
        username: username,
        password: password,
        confirm_password: confirmPassword
    };

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/users/register",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(userData)
            }
        );

        const data = await response.json();

        console.log("Status:", response.status);
        console.log("Response:", data);

        if (!response.ok) {
            alert(data.detail);
            return;
        }

        alert("Registration successful!");

        window.location.href = "login.html";

    } catch (error) {
        console.error("Error:", error);
        alert("Could not connect to the server.");
    }
});