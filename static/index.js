const loadBtn = document.querySelector(".fetch-videos");
const playlist_url = document.querySelector("#playlist_url");
const playlistBox = document.querySelector(".main-playlist-box");

const downloadBtn = document.querySelector("#download-btn");
const musicInput = document.querySelector("#music");

const errorMessageContainer = document.querySelector(
  ".error-message-container"
);
const errorMessage = document.querySelector("#error-mess");

let successfulLoad = true;

downloadBtn.disabled = true;

const downloadSuccessBtn = () => {
  playlistBox.classList.remove("downloading-animation");
  downloadBtn.innerText = "SUCCESS!";
  downloadBtn.classList.remove("btn-normal");
  downloadBtn.classList.add("btn-success");
};

const resetErrorMessage = () => {
  downloadBtn.disabled = true;
  downloadBtn.classList.remove("btn-success");
  downloadBtn.classList.remove("btn-normal");
  downloadBtn.classList.add("btn-disabled");

  loadBtn.disabled = true;
  loadBtn.classList.remove("btn-normal");
  loadBtn.classList.add("btn-disabled");

  errorMessage.value = "";
  errorMessageContainer.style.visibility = "hidden";

  playlistBox.classList.add("downloading-animation");
  downloadBtn.innerText = "DOWNLOAD PLAYLIST";
};

const showErrorMessage = (errorMess) => {
  playlistBox.classList.remove("downloading-animation");
  playlist_url.value = "";

  loadBtn.disabled = false;
  loadBtn.classList.add("btn-normal");
  loadBtn.classList.remove("btn-disabled");

  errorMessage.innerText = errorMess;
  errorMessageContainer.style.visibility = "visible";
};

const handlePlaylistBox = (action, data) => {
  if (action == "show") {
    document.querySelector(".playlist-info").innerHTML = `
        <p>Playlist title: ${data[0]}</p>
        <p>Videos count:  ${data[1]}</p>
      `;
    document.querySelector(
      ".playlist-image"
    ).style.backgroundImage = `url(${data[2]})`;
  } else if (action == "reset") {
    document.querySelector(".playlist-info").innerHTML = `
  <p>Playlist title:</p>
  <p>Videos count:</p>
`;
    document.querySelector(".playlist-image").style.backgroundImage = `none`;
  }
};

const loadPlaylistInfo = (event) => {
  event.preventDefault();

  resetErrorMessage();

  fetch("/load", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `playlist_url=${playlist_url.value}`,
  })
    .then((response) => response.json())
    .then((data) => {
      successfulLoad = true;

      handlePlaylistBox("show", data);

      playlistBox.classList.remove("downloading-animation");

      loadBtn.disabled = false;
      loadBtn.classList.add("btn-normal");
      loadBtn.classList.remove("btn-disabled");

      downloadBtn.disabled = false;
      downloadBtn.classList.add("btn-normal");
      downloadBtn.classList.remove("btn-disabled");
    })
    .catch((error) => {
      link = playlist_url.value;

      successfulLoad = false;

      if (link == "") {
        showErrorMessage("Please provide a link");
      } else if (link.length < 72) {
        showErrorMessage("Please provide a valid link");
      } else {
        showErrorMessage(
          "Playlist cannot be loaded, check if private or try again later"
        );
      }

      handlePlaylistBox("reset");
    });
};

const downloadPlaylistLoader = (event) => {
  event.preventDefault();

  if (successfulLoad == false) {
    return;
  }

  loadBtn.disabled = true;
  loadBtn.classList.remove("btn-normal");
  loadBtn.classList.add("btn-disabled");

  playlistBox.classList.add("downloading-animation");
  downloadBtn.disabled = true;
  downloadBtn.classList.remove("btn-normal");
  downloadBtn.classList.add("btn-disabled");

  fetch("/download", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Accept: "application/json",
    },
    body: `playlist_url=${playlist_url.value}&source_check=${
      musicInput.checked == true ? "music" : "video"
    }`,
  })
    .then((data) => {
      loadBtn.disabled = false;
      loadBtn.classList.add("btn-normal");
      loadBtn.classList.remove("btn-disabled");

      downloadSuccessBtn();
    })
    .catch((error) => {
      showErrorMessage("Error fetching videos, please try again later");
    });
};

loadBtn.addEventListener("click", loadPlaylistInfo);
downloadBtn.addEventListener("click", downloadPlaylistLoader);
