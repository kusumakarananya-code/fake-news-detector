async function checkNews() {
  let news = document.getElementById("newsInput").value;

  let res = await fetch("http://localhost:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ news })
  });

  let data = await res.json();
  document.getElementById("result").innerText = data.prediction + " (" + data.confidence + "%)";

document.getElementById("result").innerHTML = `
  <b>${data.prediction}</b><br>
  Confidence: ${data.confidence}%
`;
}

try {
  let res = await fetch("http://localhost:5000/predict", {...});
  let data = await res.json();
} catch (err) {
  alert("Server error. Please try again.");
}