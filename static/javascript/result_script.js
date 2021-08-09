
// VARIABLES

var syllableVisibility = "unvisible";
var translitVisibility = "unvisible";
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
        var hrefAtt = downloadLink.getAttribute("href");
        var ending
        if (hrefAtt.includes(".xml")) {
            ending = "xml";
        }else {
            ending = "txt";
        };
        var pattern = document.getElementById("pattern").innerText;
        var result_number = document.getElementById("result-number").innerText;
        var fileName = `${language}_${pattern}_${result_number}.${ending}`
        downloadLink.setAttribute("download", fileName);
        downloadLink.click();
}


if (language === "Latin") {
    translitCheck = document.getElementById("translit-check");
    translitCheck.setAttribute("disabled", "disabled");
}

if (language != "Greek") {
    document.getElementById("show-syllable-check").setAttribute("disabled", "disabled")
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
document.getElementById("show-syllable-check").addEventListener("change", () => {
    var container = document.getElementById("syllabification-container");
    if (syllableVisibility === "unvisible") {
        syllableVisibility = "visible";
        console.log("listener");
        container.style.display = "block";
    } else if (syllableVisibility === "visible") {
        syllableVisibility = "unvisible";
        container.style.display = "none";
    };
});

document.getElementById("translit-check").addEventListener("change", () => {
    var container = document.getElementById("transliteration-container");
    if (translitVisibility === "unvisible") {
        translitVisibility = "visible";
        console.log("listener");
        container.style.display = "block";
    } else if (translitVisibility === "visible") {
        translitVisibility = "unvisible";
        container.style.display = "none";
    };
});