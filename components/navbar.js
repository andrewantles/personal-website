let pages = [
  {
    title: "Home",
    link: "index"
  }, 
  {
    title: "Blog",
    link: "blog"
  }, 
  {
    title: "Resume",
    link: "resume"
  }, 
  {
    title: "About",
    link: "about"
  }
]


function addNavbarElement(pages) {
  let navbar = document.getElementById("navbar");

  for (page in pages) {
    pageTitle = pages[page]["title"]
    pageLinkKey = pages[page]["link"]
    pageLink = "./".concat(pageLinkKey).concat(".html");

    let newPageNav = document.createElement("span");
    let newPageLink = document.createElement("a");
    
    newPageLink.setAttribute("href", pageLink)
    newPageLink.innerHTML = pageTitle;
    newPageNav.appendChild(newPageLink);

    navbar.appendChild(newPageNav);
  }

}

addNavbarElement(pages);