let posts = [
  {
    title: "Mar 1, 2024",
    link: "blog"   }]
    /*link: "2024-03-01"
  }, 
  {
    title: "2",
    link: "resume"
  }, 
  {
    title: "3",
    link: "about"
  }
]
*/

function addBlogMenuElement(posts) {
  let blogMenu = document.getElementById("blog-menu");
  blogMenu.setAttribute("top-margin", "0px")

  for (post in posts) {
    postTitle = posts[post]["title"]
    postLinkKey = posts[post]["link"]
    postLink = "./".concat(postLinkKey).concat(".html");

    let newPostNav = document.createElement("span");
    let newPostLink = document.createElement("a");
    
    newPostLink.setAttribute("href", postLink)
    newPostLink.innerHTML = postTitle;
    newPostNav.appendChild(newPostLink);

    blogMenu.appendChild(newPostNav);
  }
}

addBlogMenuElement(posts);