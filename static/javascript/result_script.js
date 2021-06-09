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



orderForm = document.getElementById("order-form");
document.getElementById("order-check-reverse").addEventListener("change", () => {
    
    orderForm.submit();
});

document.getElementById("order-check-descending").addEventListener("change", () => {
    orderForm.submit();
});

