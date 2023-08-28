const loadBtn = document.querySelector("#fetch-videos");

const playlist_url = document.querySelector("#playlist_url");

const loadPlaylistInfo = (event) => {
  event.preventDefault();

  fetch("/load", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `playlist_url=${playlist_url.value}`,
  })
    .then((response) => response.json())
    .then((data) => {
      document.querySelector(".playlist-info").innerHTML = `
        <p>Playlist title: ${data[0]}</p>
        <p>Videos count:  ${data[1]}</p>
      `;
      document.querySelector(
        ".playlist-image"
      ).style.backgroundImage = `url(${data[2]})`;
    })
    .catch((error) => {
      console.error("Error fetching videos:", error);
    });
};

loadBtn.addEventListener("click", loadPlaylistInfo);
