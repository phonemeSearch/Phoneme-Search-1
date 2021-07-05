
// DATA STRUCTURES

consonants_greek = ""
vowels_greek = ""
/*sylables_greek = [
                    `^(\\${C}{1,2})?\\${V}\\${V}\\${V}`,
                    `^(\\${C}{1,2})?\\${V}\\${V}\\${C}`,
                    `^(\\${C}{1,2})?\\${V}\\${C}\\${V}`,
                    `^(\\${C}{1,2})?\\${V}\\${C}\\${C}`
                ]

*/
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
