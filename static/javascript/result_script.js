
// VARIABLES

var syllableVisibility = "visible";
var translitVisibility = "visible";
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

if (["Armenian", "Greek"].includes(language)) {
    console.log("syllab");
    document.getElementById("syllable-check").removeAttribute("disabled");
};

document.getElementById("syllable-check").addEventListener("change", () => {
    var syllabs = document.getElementsByClassName("syllab");
    console.log("vis")
    if (syllableVisibility === "unvisible") {
        syllableVisibility = "visible";
        for (var i=0, max=syllabs.length; i<max; i++) {
            syllabs[i].style.visibility = "visible";
        };
    } else if (syllableVisibility === "visible") {
        syllableVisibility = "unvisible";
        for (var i=0, max=syllabs.length; i<max; i++) {
            syllabs[i].style.visibility = "hidden";
        };
    };
});

document.getElementById("translit-check").addEventListener("change", () => {
    var translits = document.getElementsByClassName("translit");
    if (translitVisibility === "unvisible") {
        translitVisibility = "visible";
        for (var i=0; i<=translits.length; i++) {
            translits[i].style.visibility = "visible";
        };
    } else if (translitVisibility === "visible") {
        translitVisibility = "unvisible";
        for (var i=0; i<=translits.length; i++) {
            translits[i].style.visibility = "hidden";
        };
    };
});

const pageForm = document.getElementById("page-form")
pageForm.addEventListener("submit", (event)=>{
    userPage = parseInt(document.getElementById("page-input").value);
    pages = parseInt(document.getElementById("pages").innerText);

    if (userPage > pages) {
        /*document.getElementById("page-input").style.borderColor = "rgb(200, 100, 100)";
        warning = document.createElement("span")
        warning.setAttribute("id", "warning");
        warning.innerText = `Page number too big, there are only ${pages} pages.`
        pageForm.append(warning);*/
        event.preventDefault();
    } else {
        document.getElementById("page-form").submit();
    }
});
