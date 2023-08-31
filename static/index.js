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

const handlePlaylistBox = (action, data) => {
  if (action == "show") {
    document.querySelector(".playlist-info").innerHTML = `
        <p>Playlist title: ${data["playlist_title"]}</p>
        <p>Total videos:  ${data["playlist_length"]}</p>
      `;
    document.querySelector(
      ".playlist-image"
    ).style.backgroundImage = `url(${data["playlist_image"]})`;
  } else if (action == "reset") {
    document.querySelector(".playlist-info").innerHTML = `
  <p>Playlist title:</p>
  <p>Total videos:</p>
`;
    document.querySelector(".playlist-image").style.backgroundImage = `none`;
  }
};

const resetErrorMessage = () => {
  disableBtn("download");
  disableBtn("load");

  errorMessage.value = "";
  errorMessageContainer.style.visibility = "hidden";

  playlistBox.classList.add("downloading-animation");
  downloadBtn.innerText = "DOWNLOAD PLAYLIST";
};

const showErrorMessage = (errorMess) => {
  playlistBox.classList.remove("downloading-animation");
  playlist_url.value = "";

  enableBtn("load");

  errorMessage.innerText = errorMess;
  errorMessageContainer.style.visibility = "visible";
};

const downloadSuccessBtn = () => {
  playlistBox.classList.remove("downloading-animation");
  downloadBtn.innerText = "DOWNLOADS FOLDER";
  downloadBtn.classList.remove("btn-normal");
  downloadBtn.classList.add("btn-success");
};

const disableBtn = (type) => {
  if (type == "load") {
    loadBtn.disabled = true;
    loadBtn.classList.remove("btn-normal");
    loadBtn.classList.add("btn-disabled");
  } else if (type == "download") {
    downloadBtn.disabled = true;
    downloadBtn.classList.remove("btn-normal");
    downloadBtn.classList.add("btn-disabled");

    if (downloadBtn.classList.contains("btn-success")) {
      downloadBtn.classList.remove("btn-success");
    }
  }
};

const enableBtn = (type) => {
  if (type == "load") {
    loadBtn.disabled = false;
    loadBtn.classList.add("btn-normal");
    loadBtn.classList.remove("btn-disabled");
  } else if (type == "download") {
    downloadBtn.disabled = false;
    downloadBtn.classList.add("btn-normal");
    downloadBtn.classList.remove("btn-disabled");

    if (downloadBtn.classList.contains("btn-success")) {
      downloadBtn.classList.remove("btn-success");
    }
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

      enableBtn("load");
      enableBtn("download");
    })
    .catch((error) => {
      link = playlist_url.value;

      successfulLoad = false;

      if (link == "") {
        showErrorMessage("Please provide a link");
      } else if (link.length == 72) {
        showErrorMessage(
          "Playlist cannot be loaded, check if private or try again later"
        );
      } else {
        showErrorMessage("Please provide a valid link");
      }

      handlePlaylistBox("reset");
    });
};

const downloadPlaylistLoader = (event) => {
  event.preventDefault();

  if (successfulLoad == false) {
    return;
  }

  disableBtn("load");
  disableBtn("download");

  playlistBox.classList.add("downloading-animation");

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
      enableBtn("load");
      downloadSuccessBtn();
    })
    .catch((error) => {
      showErrorMessage("Error fetching videos, please try again later");
    });
};

loadBtn.addEventListener("click", loadPlaylistInfo);
downloadBtn.addEventListener("click", downloadPlaylistLoader);
