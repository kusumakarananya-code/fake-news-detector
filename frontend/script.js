async function checkNews() {
  let news = document.getElementById("newsInput").value;

  let res = await fetch("https://fake-news-detector-7-j6ru.onrender.com/predict", {
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
  let res = await fetch("https://fake-news-detector-7-j6ru.onrender.com", {...});
  let data = await res.json();
} catch (err) {
  alert("Server error. Please try again.");
}

async function checkURL(){
 let url = document.getElementById("urlInput").value;

 let res = await fetch("https://fake-news-detector-7-j6ru.onrender.com/check_url", {
   method:"POST",
   headers:{"Content-Type":"application/json"},
   body: JSON.stringify({url})
 });

 let data = await res.json();
 alert(data.prediction);
}