// ================= NEWS CHECK =================
async function checkNews() {

  let news = document.getElementById("newsInput").value;

  if (!news) {
    alert("Please enter news text");
    return;
  }

  try {

    let res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ news: news })
    });

    let data = await res.json();

    document.getElementById("result").innerHTML = `
      <b style="color:${data.prediction === "Fake" ? "red" : "lime"}">
        ${data.prediction}
      </b><br>
      Confidence: ${data.confidence}%
    `;

  } catch (err) {

    alert("Server error. Please try again.");
    console.error(err);

  }
}



// ================= URL CHECK =================
async function checkURL() {

  let url = document.getElementById("urlInput").value;

  if (!url) {
    alert("Enter URL first");
    return;
  }

  try {

    let res = await fetch("/check_url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url })
    });

    let data = await res.json();

    alert("Prediction: " + data.prediction);

  } catch (err) {

    alert("Error checking URL");
    console.error(err);

  }

}



// ================= REGISTER =================
async function register() {

  let username = document.getElementById("regUser").value;
  let password = document.getElementById("regPass").value;

  if (!username || !password) {

    alert("Enter username and password");
    return;

  }

  try {

    let res = await fetch("/register", {

      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        username: username,
        password: password
      })

    });

    let data = await res.json();

    alert(data.msg);

  } catch (err) {

    alert("Registration failed");
    console.error(err);

  }

}