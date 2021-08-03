
// VARIABLES

var visibility = "unvisible";
var language = document.getElementById("searched-lang").innerText;

console.log(language);

const nextButton = document.getElementById("next-btn");
const lastButton = document.getElementById("last-btn");
var pages = document.getElementById("pages").innerText;
var pageNum = document.getElementById("page-num-visible").innerText;


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

// download txt-file
if (document.getElementById("download-status")) {
        console.log("download");
        const downloadLink = document.getElementById("download-link-id");
        var pattern = document.getElementById("pattern").innerText;
        var result_number = document.getElementById("result-number").innerText;
        var fileName = `${language}_${pattern}_${result_number}.txt`
        downloadLink.setAttribute("download", fileName);
        downloadLink.click();
}


if (language == "Greek") {
    const orderSection = document.getElementById("order-section-id");
    const syllableContainer = document.createElement("div");
    const downloadContainer = document.getElementById("download-container");
    const separator = document.createElement("hr");
    syllableContainer.setAttribute("id", "syllable-container");
    const showSyllableCheck = document.createElement("input");
    const syllableLabel = document.createElement("label");
    syllableLabel.setAttribute("for", "show-syllable-check");
    syllableLabel.innerText = "show syllables";
    showSyllableCheck.setAttribute("id", "show-syllable-check");
    showSyllableCheck.setAttribute("type", "checkbox");
    syllableContainer.append(showSyllableCheck, syllableLabel);
    orderSection.insertBefore(syllableContainer, downloadContainer);
    orderSection.insertBefore(separator, downloadContainer);

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