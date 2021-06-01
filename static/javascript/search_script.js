// code for add phoneme expand
// with click on plus-button new text input appears along with
// minus-button and add button
function removeDisabled(id) {
    console.log(id);
    document.getElementById(id).removeAttribute("disabled");
}

function addToSearch(inputContent) {
    const searchInput = document.getElementById("user-input");
    searchInput.value += inputContent;
    document.getElementById("add-phoneme-container").remove();
    removeDisabled(id="plus-button");
}

document.getElementById("plus-button").addEventListener("click", e => {
    var addContainer = document.createElement("div");
    var addInput = document.createElement("input");
    var addBtn = document.createElement("button");
    var delBtn = document.createElement("button");

    addContainer.setAttribute("id", "add-phoneme-container");
    addContainer.setAttribute("class", "form-part-wrapper");
    addInput.setAttribute("class", "text-field");
    addInput.setAttribute("id", "add-input-field");
    addBtn.setAttribute("type", "button");
    addBtn.setAttribute("id", "add-button");
    addBtn.textContent = "add";
    delBtn.setAttribute("type", "button");
    delBtn.setAttribute("id", "minus-button");
    delBtn.textContent = "-";

    addContainer.append(delBtn, addInput, addBtn);
    document.getElementById("search-form").append(addContainer);

    document.getElementById("add-input-field").addEventListener ("keypress", e => {
        wrongInputHandle(e=e, pressed=e.key, fieldId="add-input-field");
    });

    document.getElementById("add-button").addEventListener("click", () => {
       addToSearch(inputContent=document.getElementById("add-input-field").value);
    });

    document.getElementById("minus-button").addEventListener("click", () =>{
        document.getElementById("add-phoneme-container").remove();
        document.getElementById("plus-button").removeAttribute("disabled");
    });

    document.getElementById("plus-button").setAttribute("disabled", "disabled");
});


//code for wrong input handling
function wrongInput(errorMessage, fieldId) {
    var inputField = document.getElementById(fieldId);
    inputField.setAttribute("class", "text-field-wrong");
    var infoContainer = document.createElement("div");
    infoContainer.setAttribute("id", "wrong-message-id");
    infoContainer.setAttribute("class", "wrong-message");
    infoContainer.innerText = errorMessage;
    const inputContainer = document.getElementById("user-input-container");
    inputContainer.append(infoContainer);
}

function wrongInputHandle(e, pressed, fieldId) {
    if (document.getElementById("wrong-message-id")) {
        document.getElementById("wrong-message-id").remove();
        document.getElementById(fieldId).setAttribute("class", "text-field");
    }
    var greekForbidden = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', 'A', 'C', 'F', 'H', 'J', 'K', 'L', 'N', 'P',
                          'R', 'V', 'W', '|', 'y', 'a', 'e', 'ē', 'ē', 'y', 'o', 'ō', 'i', 'a', 'e', 'o', 'ō', 'i', 'u',
                          'u', 'p', 'b', 'ph', 't', 'd', 'th', 'k', 'g', 'kh', 'ks', 'dz', 'm', 'n', 'l', 'r', 's', 's',
                          'ps'];
    var vedicForbidden = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', 'A', 'C', 'F', 'H', 'J', 'K', 'L', 'N', 'P',
                          'R', 'V', 'W', 'X', '|', 'a', 'á', 'à', 'ā', 'e', 'é', 'è', 'i', 'ì', 'í', 'ī', 'o', 'ò', 'u',
                          'ù', 'ú', 'p', 'ph', 'b', 'bh', 't', 'th', 'd', 'dh', 'ṭ', 'ṭh', 'ḍ', 'ḍh', 'k', 'kh', 'g',
                          'gh', 'c', 'ch', 'j', 'v', 'y', 'm', 'ṃ', 'n', 'ṇ', 'l', 'r', 's', 'ṣ', 'ś', 'h'];
    var language = document.getElementById("choose-language-id").value;
    console.log(language);
    if (language == "1") {
        if (greekForbidden.includes(pressed)) {
            console.log("pass")
        } else {
            var message = "character '" + pressed + "' is no allowed input for Greek";
            e.preventDefault();
            wrongInput(errorMessage=message, fieldId=fieldId);
        }
    } else if (language == "2") {
        if (vedicForbidden.includes(pressed)) {
            console.log("pass")
        } else {
            var message = "character '" + pressed + "' is no allowed input for Vedic";
            e.preventDefault();
            wrongInput(errorMessage=message, fieldId=fieldId);
        }
    }
}

document.getElementById("user-input").addEventListener("keypress", e => {
    var existing = document.getElementById("add-input-field");
    if (existing != null) {
        document.getElementById("add-input-field").setAttribute("class", "text-field");
    }
    wrongInputHandle(e=e, pressed=e.key, fieldId="user-input");
});

//show key expand
var chooseDropdown = document.getElementById("choose-language-id");
chooseDropdown.addEventListener("change", () => {
    var existing = document.getElementById("key-container");
    if (existing != null) {
        var indicationVector = document.getElementById("key-vector");
        indicationVector.style.transform = "rotate(180deg)";
        existing.remove();
    }
});

chooseDropdown.addEventListener("change", () => {
    var existing = document.getElementById("keyboard-container");
    if (existing != null) {
        var indicationVector = document.getElementById("keyboard-vector");
        indicationVector.style.transform = "rotate(180deg)";
        existing.remove();
    }
    });

const phonemesGreek = {
    "a": " α", "e": " ε", "ē": " η", "i": " ι", "o": " ο", "ō": " ω", "y": " υ", "u": " ου", "a": " ά", "e": " έ",
    "i": " ί", "o": " ό", "ō": " ώ", "y": " ύ", "u": " όυ", "ē": " ή", "i": " ι", "p": " π", "b": " β", "ph": "φ",
    "t": " τ", "d": " δ", "th": "θ", "k": " κ", "g": " γ", "kh": "χ", "z": " ζ", "m": " μ", "n": " ν", "l": " λ",
    "r": " ρ", "s": " σ", "s": " ς", "ps": "ψ", "p": " π", "b": " β", "ph": "φ", "t": " τ", "d": " δ", "th": "θ",
    "k": " κ", "g": " γ", "ks": "ξ"};

const featuresGreek = {"A": "alveolar", "L": "labial", "K": "velar", "J": "palatal", "G": "laryngeal",
           "P": "plosive", "R": "approximant", "W": "sonorant", "N": "nasal", "F": "fricative", ">": "voiced",
           "#": "aspirated", "<": "voiceless", "%": "not aspirated", "C": "consonant", "V": "vowel"};

const phonemesVedic = {"a": "b"};
const featuresVedic = {"A": "B"};

const wildcards = {"*": "0 or more characters", "|": "marks end of lemma"};

var showKey = document.getElementById("expand-key-button");
showKey.addEventListener("click", () => {    
    var indicationVector = document.getElementById("key-vector");
    var existing = document.getElementById("key-container");
    if (existing != null) {
        console.log(existing);
        indicationVector.style.transform = "rotate(180deg)";
        existing.remove();

    } else {
        //var line = document.createElement("li");
        //var entry = document.createTextNode(node);
        indicationVector.style.transform = "none";
        var keyContainer = document.createElement("div");
        keyContainer.setAttribute("id", "key-container");
        keyContainer.setAttribute("class", "expand-container");

        for (var count=0; count<=2; count++) {
            var keyKind;
            const greek = [phonemesGreek, featuresGreek, wildcards];
            const vedic = [phonemesVedic, featuresVedic, wildcards];
            const header = ["phonemes", "features", "wildcards"];
            language = document.getElementById("choose-language-id").value;
            if (language === "1") {
                keyKind = greek[count];
                kindHeader = header[count];

            } else if (language === "2") {
                keyKind = vedic[count];
                kindHeader = header[count];
            }
            var list = document.createElement("ol");
            var headerLine = document.createElement("li");
            headerLine.innerText = kindHeader;
            list.append(headerLine);
            console.log(keyKind);
            for (var [key, value] of Object.entries(keyKind)) {
                var node = (key + ": " + value);
                var line = document.createElement("li");
                line.innerText = node;
                list.append(line);
            }
            keyContainer.append(list);
        }
        var expandContainer = document.getElementById("expand-key-section");
        expandContainer.append(keyContainer);
    }
});

//show keyboard expand
var showKeyboard = document.getElementById("expand-keyboard-button")
showKeyboard.addEventListener("click", () => {
    var existing = document.getElementsByClassName("key");
    if (existing.length != 0) {
        document.getElementById("keyboard-vector").style.transform = "rotate(180deg)";
        document.getElementById("keyboard-container").remove();
    } else {
        document.getElementById("keyboard-vector").style.transform = "none";
        var keyboardContainer = document.createElement("div");
        keyboardContainer.setAttribute("id", "keyboard-container");
        keyboardContainer.setAttribute("class", "expand-container");
        var language = document.getElementById("choose-language-id").value;
        var specialCharsGreek = {"á": "1", "é": "2", "í": "3"};
        var specialCharsVedic = {"á": "1", "é": "2", "í": "3"};
        greek = [featuresGreek, specialCharsGreek];
        vedic = [featuresVedic, specialCharsVedic];

        for (var count=0; count<=1; count++) {
            var kind;
            if (language === "1") {
                kind = greek[count];
            } else if (language === "2") {
                kind = vedic[count];
            }
            innerContainer = document.createElement("div");
            innerContainer.setAttribute("class", "inner-key-container");
            console.log(kind);
            for (var [e, value] of Object.entries(kind)) {
                var spanKey = document.createElement("span");
                spanKey.setAttribute("class", "key-span");
                var btnKey = document.createElement("button");
                btnKey.innerText = e;
                btnKey.setAttribute("class", "key");
                spanKey.append(btnKey);
                keyboardContainer.append(spanKey);
            };
            keyboardContainer.append(innerContainer);
        }
        document.getElementById("expand-keyboard-section").append(keyboardContainer);
    }
});
