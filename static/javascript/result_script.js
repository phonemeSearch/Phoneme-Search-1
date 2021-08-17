
// VARIABLES

var syllableVisibility = "unvisible";
var translitVisibility = "unvisible";
var language = document.getElementById("searched-lang").innerText;
//var resultForm = document.getElementById("result-form");

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

if (["armenian", "greek"].includes(language)) {
    console.log("syllab");
    document.getElementById("syllable-check").removeAttribute("disabled");
}

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