

function buildHeader () {
  header = document.getElementById("header");
  let headerText = document.createElement("h1");
  headerText.innerHTML = "Andrew Antles' Personal Site";
  header.appendChild(headerText);
}

buildHeader();
