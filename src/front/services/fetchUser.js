export const fetchLogin = async (email, password) => {
  try {
    if (password.trim() === "" || email.trim() === "") {
      throw new Error("the fields cannot be empty");
    }
    const rawData = JSON.stringify({
      email: email,
      password: password,
    });
    const response = await fetch(
      "https://ideal-cod-695g4vw6rr4whrr7-3001.app.github.dev/api/login",
      {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: rawData,
      }
    );
    console.log(rawData);
    if (!response.ok) {
      throw new Error(`Error fetching data code:${response.status}`);
    }
    const data = await response.json();

    const token = JSON.stringify(data.token);

    localStorage.setItem("token", token);
  } catch (error) {
    console.error(error);
  }
};
