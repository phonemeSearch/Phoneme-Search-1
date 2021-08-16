
// VARIABLES

var syllableVisibility = "unvisible";
var translitVisibility = "unvisible";
var language = document.getElementById("searched-lang").innerText;
var resultForm = document.getElementById("result-form");

console.log(language);

const nextButton = document.getElementById("next-btn");
const lastButton = document.getElementById("last-btn");
var pages = document.getElementById("pages").innerText;
var pageNum = document.getElementById("page-input").value;


//document.getElementById("skip-direction").value = "";
//console.log(document.getElementById("skip-direction").value);

if (parseInt(pageNum) === parseInt(pages)) {
    nextButton.setAttribute("disabled", "disabled");
} else{
    nextButton.removeAttribute("disabled");
}

if (parseInt(pageNum) <= 1) {
    lastButton.setAttribute("disabled", "disabled");
} else {
    lastButton.removeAttribute("disabled");
};


document.getElementById("reverse-check").addEventListener("change", () => {
    document.getElementById("order-form").submit();
});

document.getElementById("descending-check").addEventListener("change", () => {
    document.getElementById("order-form").submit();
});

if (language === "Latin") {
    translitCheck = document.getElementById("translit-check");
    translitCheck.setAttribute("disabled", "disabled");
}

if (["Armenian", "Greek"].includes(language)) {
    console.log("syllab");
    document.getElementById("syllable-check").removeAttribute("disabled");
}
    /*const orderSection = document.getElementById("order-section-id");
    const syllableContainer = document.createElement("div");
    const downloadContainer = document.getElementById("download-container");
    syllableContainer.setAttribute("id", "syllable-container");
    const showSyllableCheck = document.createElement("input");
    const syllableLabel = document.createElement("label");
    syllableLabel.setAttribute("for", "show-syllable-check");
    syllableLabel.innerText = "show syllables";
    showSyllableCheck.setAttribute("id", "show-syllable-check");
    showSyllableCheck.setAttribute("type", "checkbox");
    syllableContainer.append(showSyllableCheck, syllableLabel);
    orderSection.insertBefore(syllableContainer, downloadContainer);
*/
document.getElementById("syllable-check").addEventListener("change", () => {
    var container = document.getElementById("syllabification-container");
    if (syllableVisibility === "unvisible") {
        syllableVisibility = "visible";
        console.log("listener");
        container.style.visibility = "visible";
    } else if (syllableVisibility === "visible") {
        syllableVisibility = "unvisible";
        container.style.visibility = "hidden";
    };
});

document.getElementById("translit-check").addEventListener("change", () => {
    var container = document.getElementById("transliteration-container");
    if (translitVisibility === "unvisible") {
        translitVisibility = "visible";
        console.log("listener");
        container.style.visibility = "visible";
    } else if (translitVisibility === "visible") {
        translitVisibility = "unvisible";
        container.style.visibility = "hidden";
    };
});

resultForm.addEventListener("submit", () => {
    console.log("user text");
    var pageNum = document.getElementById("pages").innerText;
    pageNum = parseInt(pageNum);
    var currentPage = document.getElementById("curr-page");
    var userNum = document.getElementById("page-input").value;
    currentPage.value = userNum;
    userNum = parseInt(userNum);
    console.log(userNum, pageNum);
    if (userNum <= pageNum) {
        userNum = (userNum-1)*25;
        console.log(userNum);
        var currentOffset = document.getElementById("curr-offset");
        currentOffset.value = userNum;
        console.log(currentOffset.value);
        //document.getElementById("skip-direction").value = "false";
        document.getElementById("result-form").submit();
    } else {

    };
});

nextButton.addEventListener("click", () => {
    console.log("next");
    var skipDirection = document.getElementById("skip-direction");
    skipDirection.value = "next";
    console.log("btn val", skipDirection.value);
    resultForm.submit();
});

lastButton.addEventListener("click", () => {
    console.log("last");
    var skipDirection = document.getElementById("skip-direction");
    skipDirection.value = "last";
    console.log("btn val", skipDirection.value);
    resultForm.submit();
});

document.getElementById("download-txt-button").addEventListener("click", () => {
    console.log("down txt")
    var downInput = document.getElementById("download-input");
    downInput.value = "txt";
    resultForm.submit();
});

document.getElementById("download-xml-button").addEventListener("click", () => {
    var downInput = document.getElementById("download-input");
    downInput.value = "xml";
    resultForm.submit();
});
