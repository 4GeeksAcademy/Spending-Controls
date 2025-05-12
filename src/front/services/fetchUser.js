const backendUrl = import.meta.env.VITE_BACKEND_URL;

export const fetchLogin = async (email, password) => {
  try {
    if (password.trim() === "" || email.trim() === "") {
      throw new Error("the fields cannot be empty");
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(email)) {
      throw new Error("Invalid email format");
    }

    if (password.length < 8) {
      throw new Error("The password must have at least 8 characters");
    }

    const rawData = JSON.stringify({
      email: email,
      password: password,
    });
    const response = await fetch(`${backendUrl}api/login`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: rawData,
    });
    console.log(rawData);

    if (!response.ok) {
      throw new Error(`Error fetching data code:${response.status}`);
    }
    if (!response.token) {
      throw new Error("The token has not been sent correctly to the user");
    }
    const data = await response.json();

    const token = JSON.stringify(data.token);

    localStorage.setItem("token", token);
  } catch (error) {
    console.error(error);
  }
};
