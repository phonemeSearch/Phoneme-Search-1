
// DATA STRUCTURES

var visibility = "unvisible";


var language = document.getElementById("searched-lang").innerText;

const nextButton = document.getElementById("next-btn");
const lastButton = document.getElementById("last-btn");
var pages = document.getElementById("pages").innerText;
var pageNum = document.getElementById("page-num").innerText;

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


if (language == "Greek") {
    const orderSection = document.getElementById("order-section-id");
    const syllableContainer = document.createElement("div");
    const downloadContainer = document.getElementById("download-container");
    syllableContainer.setAttribute("id", "syllable-container");
    const showSyllableCheck = document.createElement("input");
    const syllableLabel = document.createElement("label");
    syllableLabel.innerText = "show syllables";
    showSyllableCheck.setAttribute("id", "show-syllable-check");
    showSyllableCheck.setAttribute("type", "checkbox");
    syllableContainer.append(showSyllableCheck, syllableLabel);
    orderSection.insertBefore(syllableContainer, downloadContainer);

    document.getElementById("show-syllable-check").addEventListener("change", () => {
        var container = document.getElementById("syllabification-container");
        if (visibility == "unvisible") {
            visibility = "visible";
            console.log("listener");
            container.style.display = "block";
        } else if (visibility == "visible") {
            visibility = "unvisible";
            container.style.display = "none";
        };
    });
}