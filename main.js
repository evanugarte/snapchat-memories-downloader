// === USER CHOICES ===

let dateChoice = '';
let uploadedJsonData = null;
let uploadedFileName = '';
let use24Hr = false;

// === END USER CHOICES ===

// === HELPERS ===

const SAVED_DATA = 'Saved Media';
const DATE = 'Date';
const MEDIA_TYPE = 'Media Type';
const DOWNLOAD_LINK = 'Download Link';
const SNAPCHAT_URL = 'https://app.snapchat.com/';
const DATE_TYPES = {
  MONTH_DAY_YEAR: 'month-day-year',
  DAY_MONTH_YEAR: 'day-month-year',
  FULLY_SPELLED_OUT: 'spelt-out',
};

function formatNumber(number) {
  return number.toString().padStart(2, '0');
}

function getTime(date) {
  const convertedDate = new Date(date);
  const hours = convertedDate.getHours();
  const minutes = formatNumber(convertedDate.getMinutes());
  if (use24Hr) {
    return hours + ":" + minutes;
  } else {
    const amOrPm = hours >= 12 ? 'pm' : 'am';
    const convertedHours = (hours % 12) || 12;
    return convertedHours + ":" + minutes + " " + amOrPm;
  }
}

function fullySpeltOutDate(date) {
  const convertedDate = new Date(date);
  const MONTHS = [
    'January', 'Feburary', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  return `${MONTHS[convertedDate.getMonth()]} `
    + `${formatNumber(convertedDate.getDay() + 1)}, `
    + `${convertedDate.getFullYear()} `
    + getTime(date);
}

function dateWithSlashes(date, dayBeforeMonth = false) {
  const convertedDate = new Date(date);
  let result = '';
  if (dayBeforeMonth) {
    result += `${formatNumber(convertedDate.getDay() + 1)}/`
      + `${formatNumber(convertedDate.getMonth() + 1)}`;
  } else {
    result += `${formatNumber(convertedDate.getMonth() + 1)}/`
      + `${formatNumber(convertedDate.getDay() + 1)}`;
  }
  return result
    + `/${convertedDate.getFullYear()} `
    + getTime(date);
}

function hasAppropriateFields(element) {
  return DATE in element
    && MEDIA_TYPE in element
    && DOWNLOAD_LINK in element
    && element[DOWNLOAD_LINK].startsWith(SNAPCHAT_URL);
}

function validateJSONResults(jsonData) {
  const memoriesData = jsonData[SAVED_DATA];
  if (!memoriesData) {
    return false;
  } else {
    return memoriesData.some(hasAppropriateFields);
  }
}

function convertUrlParamsToObject(urlString) {
  return JSON.parse('{"' + decodeURI(urlString).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g, '":"') + '"}')
}

function getAppropriateDateString(date) {
  if (dateChoice === DATE_TYPES.DAY_MONTH_YEAR) {
    return dateWithSlashes(date, true);
  } else if (dateChoice === DATE_TYPES.MONTH_DAY_YEAR) {
    return dateWithSlashes(date);
  } else if (dateChoice === DATE_TYPES.FULLY_SPELLED_OUT) {
    return fullySpeltOutDate(date);
  } else {
    return date;
  }
}

async function downloadMemories(jsonData, submitButtonElement) {
  let awsCount = 0, downloadCount = 0;
  const callback = () => {
    if (awsCount === 0 || downloadCount === 0) {
      submitButtonElement.classList.add('invalid');
      submitButtonElement.textContent = 'Couldn\'t generate download links.\
      You may need to rerequest your data from Snapchat and try again.';
    } else {
      submitButtonElement.textContent =
        `${downloadCount} / ${jsonData.length} memories downloaded.`;
    }
  };
  let promises = [];
  let awsLinks = [];
  submitButtonElement.textContent = 'Generating AWS download links...';
  jsonData.forEach(async (memory) => {
    promises.push(
      fetch(memory[DOWNLOAD_LINK], {
        method: 'POST',
      })
        .then(response => response.text())
        .then((data) => {
          awsLinks.push({
            downloadLink: data,
            dateString: getAppropriateDateString(memory[DATE]),
            type: memory[MEDIA_TYPE] === 'VIDEO' ? 'mp4' : 'jpg',
          });
          awsCount++;
        })
        .catch(_ => { })
    );
  });

  await Promise.all(promises)
    .then(() => {
      submitButtonElement.textContent = 'Downloading memories...'
    })
    .catch(_ => { });

  let interval = setInterval(download, 300, awsLinks, callback);
  async function download() {
    const awsLink = awsLinks.pop();
    await fetch('https://snapchat-memory-saver-cors.herokuapp.com/'
      + awsLink.downloadLink)
      .then(response => response.blob())
      .then(blob => {
        const blobUrl = URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = blobUrl;
        a.style = "display: none";
        a.setAttribute('target', '_blank');
        a.download = awsLink.dateString + '.' + awsLink.type;
        document.body.appendChild(a);
        a.click();
        downloadCount++;
      })
      .catch();
    if (awsLinks.length == 0) {
      clearInterval(interval);
      callback();
    }
  }
}

function toggleParentDiv(toggleId) {
  const inputIds = ['spelt-out', 'month-day-year', 'day-month-year'];
  if (toggleId) {
    $('#' + toggleId).closest('.date-option')[0].classList.add('meme');
  }
  inputIds.filter(id => id !== toggleId).forEach(id => {
    $('#' + id).closest('.date-option')[0].classList.remove('meme');
  });
}

// === END HELPERS ===

// === EVENTS ===

let memoriesInputElement = document.getElementById('memories-input');
let memoriesInputButtonElement = document.getElementById('memories-input-btn');
let submitButtonElement = document.getElementById('submit-btn');
let uploadStatusElement = document.getElementById('upload-status');
let dateOptionElements = document.getElementsByClassName('date-option');
let dateInputElements = document.getElementById('date-format');
let submitDownloadElements = document.getElementById('submit-download');
let timeInputElement = document.getElementById('time-input');
let timeExampleElements = document.getElementsByClassName('time-example');
let tutorialToggleElement = document.getElementById('tutorial-toggle');
let explanationToggleElement = document.getElementById('explanation-toggle');

function toggleTimeDateAndSubmit(enable) {
  if (enable) {
    dateInputElements.classList.remove('disabled');
    submitDownloadElements.classList.remove('disabled');
  } else {
    dateInputElements.classList.add('disabled');
    submitDownloadElements.classList.add('disabled');
  }
}

function onReaderLoad(event) {
  try {
    uploadStatusElement.classList.remove('h2');
    uploadStatusElement.classList.add('h6');
    const jsonData = JSON.parse(event.target.result);
    const valid = validateJSONResults(jsonData);
    if (valid) {
      memoriesInputButtonElement.classList.remove('invalid');
      memoriesInputButtonElement.classList.add('valid');
      uploadedJsonData = jsonData;
      uploadStatusElement.textContent = uploadedFileName +
        ' successfully uploaded. (Click to upload a different file)';
      dateInputElements.classList.remove('disabled');
    } else {
      throw MediaError('bad file');
    }
  } catch (error) {
    toggleTimeDateAndSubmit(false);
    memoriesInputButtonElement.classList.remove('valid');
    memoriesInputButtonElement.classList.add('invalid');
    uploadStatusElement.textContent = uploadedFileName +
      ' isn\'t a valid json file. Please upload a different file';
  }
}

function handleFileUpload(file) {
  var reader = new FileReader();
  reader.onload = onReaderLoad;
  uploadedFileName = file.name;
  reader.readAsText(file);
}

function onChange(event) {
  if (memoriesInputElement.value) {
    handleFileUpload(event.target.files[0]);
  } else {
    toggleParentDiv('');
    toggleTimeDateAndSubmit(false);
    uploadStatusElement.classList.remove('h6');
    uploadStatusElement.classList.add('h2');
    memoriesInputButtonElement.classList.remove('valid');
    memoriesInputButtonElement.classList.remove('invalid');
    uploadStatusElement.textContent = 'No file chosen, yet.';
  }
}

function dropHandler(event) {
  try {
    if (event.dataTransfer.items) {
      handleFileUpload(event.dataTransfer.items[0].getAsFile());
    } else if (event.dataTransfer.files.length) {
      handleFileUpload(event.dataTransfer.files[0]());
    }
  } catch (error) { }
  event.preventDefault();
}

function dragOverHandler(event) {
  event.preventDefault();
}

memoriesInputButtonElement.addEventListener('click', function () {
  memoriesInputElement.click();
});

memoriesInputElement.addEventListener('change', onChange);

submitButtonElement.addEventListener('click', function () {
  $('.download-spinner').show();
  downloadMemories(uploadedJsonData[SAVED_DATA], submitButtonElement);
  $('.download-spinner').hide();
});

for (let i = 0; i < dateOptionElements.length; i++) {
  dateOptionElements[i].addEventListener("click", function (event) {
    const { id } = event.currentTarget;
    dateChoice = id;
    const div = document.querySelector(`#${id}`);
    toggleParentDiv(id);
    div.querySelectorAll('input')[0].click();
    submitDownloadElements.classList.remove('disabled');
  })
}

timeInputElement.addEventListener('change', function (event) {
  for (let i = 0; i < timeExampleElements.length; i++) {
    timeExampleElements[i].textContent =
      event.currentTarget.checked ? '15:00' : '3:00 pm';
  }
  use24Hr = event.currentTarget.checked;
});

$('.tutorial-close').on('click', function (event) {
  $('#tutorial-modal').modal("hide");
});

$('.explanation-close').on('click', function (event) {
  $('#explanation-modal').modal("hide");
});

(function () {
  toggleTimeDateAndSubmit(false);
})();
