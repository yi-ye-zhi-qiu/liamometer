fetch("https://dog.ceo/api/breeds/image/random/10")
  .then((response) => response.json())
  .then((data) => data.message)
  .then((arrayOfLinks) => addPhoto(arrayOfLinks))
  .catch((e) => console.log(e));

function addPhoto(links) {
  let gallery= document.querySelector(".gallery");

  for (let link of links) {
    let image_div = document.createElement("div");
    let image = document.createElement("img");
    image.src = link;
    image.classList.add("img-full")
    image_div.appendChild(image);
    image_div.classList.add("img-banner")
    let rating = document.createElement("div")
    let rating_text = document.createElement("p")
    rating_text.classList.add("topleft")
    rating_text.innerHTML = "40"
    rating.appendChild(rating_text)
    image_div.appendChild(rating)
    gallery.appendChild(image_div);
  }
}
