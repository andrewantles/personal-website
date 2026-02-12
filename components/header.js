

function buildHeader () {
  header = document.getElementById("header");

  let headerPic = document.createElement("img")
  headerPic.setAttribute("id", "header-pic")
  headerPic.setAttribute("src", "../public/img/profile.jpg")
  headerPic.setAttribute("alt", "Profile picture headshot of Andrew Antles")

  let headerText = document.createElement("h1");
  headerText.setAttribute("id", "header-text");
  headerText.innerHTML = "AndrewAntles.Net";
  
  header.appendChild(headerPic);
  header.appendChild(headerText);
}

buildHeader();
