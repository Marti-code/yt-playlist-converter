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

/**
 * Handle display or clear the playlist info box
 * @param {String} action - The action to perform ('show' or 'reset')
 * @param {JSON} data - the playlist info
 */
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

/**
 * Clear error message box and reset the download button
 */
const resetErrorMessage = () => {
  disableBtn("download");
  disableBtn("load");

  errorMessage.value = "";
  errorMessageContainer.style.visibility = "hidden";

  playlistBox.classList.add("downloading-animation");
  downloadBtn.innerText = "DOWNLOAD PLAYLIST";
};

/**
 * Disable the error message box with a specific message
 * @param {String} errorMess - the error message text
 */
const showErrorMessage = (errorMess) => {
  playlistBox.classList.remove("downloading-animation");
  playlist_url.value = "";

  enableBtn("load");

  errorMessage.innerText = errorMess;
  errorMessageContainer.style.visibility = "visible";
};

/**
 * Change the style of the download button upon success
 */
const downloadSuccessBtn = () => {
  let type = musicInput.checked == true ? "music" : "video";
  if (type == "music") {
    downloadBtn.innerText = "HAPPY LISTENING!";
  } else {
    downloadBtn.innerText = "JOYFUL WATCHING!";
  }

  downloadBtn.classList.remove("btn-normal");
  downloadBtn.classList.add("btn-success");
};

/**
 * Disable the button for the user to use
 * @param {String} type - type of the button ('load' or 'download')
 */
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

/**
 * Enable the button for the user to use
 * @param {String} type - type of the button ('load' or 'download')
 */
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

/**
 * Start the loader when loading files
 */
const loadPlaylistInfo = (event) => {
  event.preventDefault();

  resetErrorMessage();

  // Send a POST request to load the playlist info
  fetch("/load", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `playlist_url=${encodeURIComponent(playlist_url.value)}`,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.json();
    })
    .then((data) => {
      successfulLoad = true;

      // Display playlist info to the user
      handlePlaylistBox("show", data);

      playlistBox.classList.remove("downloading-animation");

      enableBtn("load");
      enableBtn("download");
    })
    .catch((error) => {
      console.error("Fetch error:", error.message); // Log the error
      link = playlist_url.value;

      successfulLoad = false;

      // Display a specific error message to the user
      if (link == "") {
        showErrorMessage("Please provide a link");
      } else if (link.length == 72) {
        showErrorMessage(
          "Playlist cannot be loaded, check if private or try again later"
        );
      } else {
        showErrorMessage("Please provide a valid link");
      }

      // Clear the playlist info
      handlePlaylistBox("reset");
    });
};

/**
 * Start the loader when downloading files
 */
const downloadPlaylistLoader = () => {
  // Check if the playlist load was successful
  if (successfulLoad == false) {
    return;
  }

  playlistBox.classList.add("downloading-animation");

  // Send a POST request to download the playlist
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
      downloadSuccessBtn(musicInput.checked);

      playlistBox.classList.remove("downloading-animation");
    })
    .catch((error) => {
      showErrorMessage("Error fetching videos, please try again later");
    });
};

loadBtn.addEventListener("click", loadPlaylistInfo);
downloadBtn.addEventListener("click", downloadPlaylistLoader);
