// code for add phoneme expand
// with click on plus-button new text input appears along with
// minus-button and add button

renderKey();
// renders HTML for key tables
function renderKey () {
    var language = document.getElementById("choose-language-id").value;
    const oldContainer = document.getElementById("key-container");
    if (oldContainer) {
        console.log("key container exists")
        oldContainer.remove();
    };
    const section = document.getElementById("expand-key-section");
    const keyContainer = document.createElement("div");
    keyContainer.setAttribute("id", "key-container");
    section.append(keyContainer);
    console.log(language);
    if (language === "1") {
        keyContainer.innerHTML =
            `<table class="key-table">
                <tr>
                    <th class="head-roll">Greek</th>
                    <th>labial</th>
                    <th>alveolar</th>
                    <th>velar</th>
                </tr>
                <tr>
                    <td class="phoneme-category">stops</td>
                    <td class="user-key">key: L</td>
                    <td class="user-key">key: A</td>
                    <td class="user-key">key: K</td>
                </tr>
                <tr>
                    <td>-voice <span class="user-key">key: P+&lt;</span></td>
                    <td>p</td>
                    <td>t</td>
                    <td>k</td>
                </tr>
                <tr>
                    <td>+voice <span class="user-key">key: P+&gt;</span></td>
                    <td>b</td>
                    <td>d</td>
                    <td>g</td>
                </tr>
                <tr>
                    <td>+aspirate <span class="user-key">key: P+#</span></td>
                    <td>ph</td>
                    <td>th</td>
                    <td>kh</td>
                </tr>
                <tr><td class="phoneme-category">affricate</td></tr>
                <tr>
                    <td></td>
                    <td>ps</td>
                    <td>z</td>
                    <td>ks</td>
                </tr>
                <tr><td class="phoneme-category">non stops</td></tr>
                <tr>
                    <td>nasal <span class="user-key">key: N</span></td>
                    <td>m</td>
                    <td>n</td>
                    <td></td>
                </tr>
                <tr>
                    <td>approximant <span class="user-key">key: R</span></td>
                    <td></td>
                    <td>l r</td>
                    <td></td>
                </tr>
                <tr>
                    <td>fricative <span class="user-key">key: F</span></td>
                    <td></td>
                    <td>s</td>
                    <td></td>
                </tr>
            </table>
            <div class="key-info">
                <span class=vowel>a</span>    
                <span class=vowel>á</span>
                <span class=vowel>e</span>
                <span class=vowel>é</span>
                <span class=vowel>i</span>
                <span class=vowel>í</span>
                <span class=vowel>o</span>
                <span class=vowel>ó</span>
                <span class=vowel>u</span>
                <span class=vowel>ú</span>
                <span class=vowel>y</span>
                <span class=vowel>ý</span>
                <span class=vowel>ē</span>
                <span class=vowel>ḗ</span>
                <span class=vowel>ō</span>
                <span class=vowel>ṓ</span>
            </div>
            <div class="key-info">
            <span class=wildcard>end/begin marker: |</span>
            <span class=wildcard>any character: *</span>
            </div>`;
    } else if (language === "2") {
        keyContainer.innerHTML = 
        `<table class="key-table">
        <tr>
            <th>Vedic</th>
            <th>labial</th>
            <th>alveolar</th>
            <th>retroflex</th>
            <th>palatal</th>
            <th>velar</th>
        </tr>
        <tr>
        <td class="phoneme-category">stops</td>
        <td class="user-key">key: L</td>
        <td class="user-key">key: A</td>
        <td class="user-key">key: X</td>
        <td class="user-key">key: J</td>
        <td class="user-key">key: K</td>
        </tr>
        <tr>
            <td>-voice -aspirate <span class="user-key">key: P+&lt;+%</span></td>
            <td>p</td>
            <td>t</td>
            <td>ṭ</td>
            <td></td>
            <td>k</td>
        </tr>
        <tr>
            <td>-voice +aspirate <span class="user-key">key: P+&lt;+#</span></td>
            <td>ph</td>
            <td>th</td>
            <td>ṭh</td>
            <td></td>
            <td>kh</td>
        </tr>
        <tr>
            <td>+voice -aspirate <span class="user-key">key: P+&gt;+%</span></td>
            <td>b</td>
            <td>d</td>
            <td>ḍ</td>
            <td></td>
            <td>g</td>
        </tr>
        <tr>
            <td>+voice +aspirate <span class="user-key">key: P+&gt;+#</span></td>
            <td>bh</td>
            <td>dh</td>
            <td>ḍh</td>
            <td></td>
            <td>gh</td>
        </tr>
        <tr>
            <td class="phoneme-category">affricates</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>-voice -aspirate <span class="user-key">key: P+&lt;+%</span></td>
            <td></td>
            <td></td>
            <td></td>
            <td>c</td>
            <td></td>
        </tr>
        <tr>
            <td>-voice +aspirate</td>
            <td></td>
            <td></td>
            <td></td>
            <td>ch</td>
            <td></td>
        </tr>
        <tr>
            <td>+voice -aspirate</td>
            <td></td>
            <td></td>
            <td></td>
            <td>j</td>
            <td></td>
        </tr>
        <tr>
            <td class="phoneme-category">non stops</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>glide</td>
            <td>v</td>
            <td></td>
            <td></td>
            <td>y</td>
            <td></td>
        </tr>
        <tr>
            <td>nasal</td>
            <td>m</td>
            <td>n</td>
            <td>ṇ</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>approximant</td>
            <td></td>
            <td>l r</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>fricative</td>
            <td></td>
            <td>s</td>
            <td>ṣ</td>
            <td>ś</td>
            <td></td>
        </tr>
    </table>`
    }
}


function removeDisabled(id) {
    console.log(id);
    document.getElementById(id).removeAttribute("disabled");
}

function addToSearch(inputContent) {
    const searchInput = document.getElementById("user-input");
    searchInput.value += inputContent;
    document.getElementById("add-phoneme-container").remove();
    removeDisabled("plus-button");
}

document.getElementById("plus-button").addEventListener("click", () => {
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

   /* document.getElementById("add-input-field").addEventListener ("input", e => {

    });*/

    document.getElementById("add-input-field").addEventListener ("keypress", key => {
        wrongInputHandling(key=key, pressed=key.key, fieldId="add-input-field");
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

//new version

/*
userInput = document.getElementById("user-input")
userInput.addEventListener("input", e => {
    wrongInputHandling("user-input", e)
});

function wrongInputHandling(id, e) {
    console.log(e.data);
    const greekAllowed = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', 'A', 'C', 'F', 'H', 'J', 'K', 'L', 'N', 'P',
    'R', 'V', 'W', '|', 'y', 'a', 'e', 'ē', 'ē', 'y', 'o', 'ō', 'i', 'a', 'e', 'o', 'ō', 'i', 'u',
    'u', 'p', 'b', 'ph', 't', 'd', 'th', 'k', 'g', 'kh', 'ks', 'dz', 'm', 'n', 'l', 'r', 's', 's',
    'ps'];
    const vedicAllowed = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', 'A', 'C', 'F', 'H', 'J', 'K', 'L', 'N', 'P',
    'R', 'V', 'W', 'X', '|', 'a', 'á', 'à', 'ā', 'e', 'é', 'è', 'i', 'ì', 'í', 'ī', 'o', 'ò', 'u',
    'ù', 'ú', 'p', 'ph', 'b', 'bh', 't', 'th', 'd', 'dh', 'ṭ', 'ṭh', 'ḍ', 'ḍh', 'k', 'kh', 'g',
    'gh', 'c', 'ch', 'j', 'v', 'y', 'm', 'ṃ', 'n', 'ṇ', 'l', 'r', 's', 'ṣ', 'ś', 'h'];
    var language = document.getElementById("choose-language-id").value;
    //console.log(language);
    if (language == "1") {
        var textField = document.getElementById(id).value;
        console.log("text 0 ", textField[0]);
        var char;
        for (var i=0; i<textField.length; i++) {
            console.log("index: ", i);
            //console.log("current field", textField.value);
            console.log("in loop", textField[i]);
            char = textField[i];
            console.log("char", char);
            if (greekAllowed.includes(char)) {
                console.log("pass");
            } else {
                console.log("not in allowed!")
            }
        }
        if (greekAllowed.includes(e.data)) {
            console.log("pass")
        } else {
            var message = "character '" + e.data + "' is no allowed input for Greek";
            e.preventDefault();
            wrongInput(message, id);
        }
    } else if (language == "2") {
        if (vedicAllowed.includes(e.data)) {
            console.log("pass")
        } else {
            e.preventDefault();
            wrongInput(message, id);
        }
    }
}
*/
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

//old version

function wrongInputHandling(key, pressed, fieldId) {
    if (document.getElementById("wrong-message-id")) {
        document.getElementById("wrong-message-id").remove();
        document.getElementById(fieldId).setAttribute("class", "text-field");
    }
    var allowed;

    const greekAllowed = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', 'A', 'C', 'F', 'J', 'K', 'L', 'N', 'P',
                          'R', 'V', 'W', 'Z', '|', 'y', 'a', 'e', 'ē', 'y', 'o', 'ō', 'i', 'a', 'o', 'ō', 'i', 'u',
                          'u', 'p', 'b', 'ph', 't', 'd', 'th', 'k', 'g', 'kh', 'ks', 'z', 'm', 'n', 'l', 'r', 's', 's',
                          'ps', 'h', 'Enter'];
    const vedicAllowed = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', 'A', 'C', 'F', 'H', 'J', 'K', 'L', 'N', 'P',
                          'R', 'V', 'W', 'X', 'Z', '|', 'a', 'á', 'à', 'ā', "e", 'é', 'è', 'i', 'ì', 'í', 'ī', 'o', 'ò', 'u',
                          'ù', 'ú', 'p', 'ph', 'b', 'bh', 't', 'th', 'd', 'dh', 'ṭ', 'ṭh', 'ḍ', 'ḍh', 'k', 'kh', 'g',
                          'gh', 'c', 'ch', 'j', 'v', 'y', 'm', 'ṃ', 'n', 'ṇ', 'l', 'r', 's', 'ṣ', 'ś', 'h', 'Enter'];
                          
    var language = document.getElementById("choose-language-id").value;
    console.log(language);
    if (language == "1") {
        allowed = greekAllowed;
        lang = "Greek"
    } else if (language == "2") {
        allowed = vedicAllowed;
        lang = "Vedic"
    }
    
    if (allowed.includes(pressed)) {
        if (language == "1") {
            if (pressed == "h") {
                fieldValue = document.getElementById(fieldId).value;
                lastChar = fieldValue.slice(-1);
                if ((lastChar != "p") && (lastChar != "k") && (lastChar != "t")) {
                    var message = `character 'h' only allowed after 'p', 'k', 't'`;
                    key.preventDefault();
                    wrongInput(message, fieldId);
                }
            }
        }
    } else {
        var message = `character '${pressed}' is no allowed input for ${lang}`;
        key.preventDefault();
        wrongInput(message, fieldId);
    }
}

document.getElementById("user-input").addEventListener("keypress", key => {
    var existing = document.getElementById("add-input-field");
    if (existing != null) {
        document.getElementById("add-input-field").setAttribute("class", "text-field");
    }
    wrongInputHandling(key, key.key, "user-input");
});

//show key expand
var chooseDropdown = document.getElementById("choose-language-id");
chooseDropdown.addEventListener("change", () => {
    console.log("change key")
    renderKey();
});

chooseDropdown.addEventListener("change", () => {
    var existing = document.getElementById("keyboard-container");
    if (existing != null) {
        var indicationVector = document.getElementById("keyboard-vector");
        indicationVector.style.transform = "rotate(180deg)";
        existing.remove();
    }
    });

chooseDropdown.addEventListener("change", () => {
    const userInput = document.getElementById("user-input");
    const addInput = document.getElementById("add-input-field");
    userInput.value = "";
    addInput.value = "";
});


/*const phonemesGreek = {
    "a": " α", "e": " ε", "ē": " η", "i": " ι", "o": " ο", "ō": " ω", "y": " υ", "u": " ου", "a": " ά", "é": " έ",
    "i": " ί", "o": " ό", "ō": " ώ", "y": " ύ", "u": " όυ", "ē": " ή", "i": " ι", "p": " π", "b": " β", "ph": "φ",
    "t": " τ", "d": " δ", "th": "θ", "k": " κ", "g": " γ", "kh": "χ", "z": " ζ", "m": " μ", "n": " ν", "l": " λ",
    "r": " ρ", "s": " σ", "s": " ς", "ps": "ψ", "p": " π", "b": " β", "ph": "φ", "t": " τ", "d": " δ", "th": "θ",
    "k": " κ", "g": " γ", "ks": "ξ"
}; */
const featuresGreek = {
    "A": "alveolar", "L": "labial", "K": "velar", "J": "palatal",
    "P": "plosive", "R": "approximant", "W": "sonorant", "N": "nasal", "F": "fricative", ">": "voiced",
    "#": "aspirated", "<": "voiceless", "%": "not aspirated", "C": "consonant", "V": "vowel"
};

//const phonemesVedic = {"a": "b"};
const featuresVedic = {
    "A": "alveolar", "L": "labial", "K": "velar", "J": "palatal",
    "P": "plosive", "R": "approximant", "W": "sonorant", "N": "nasal", "F": "fricative", "H": "laryngeal", "X": "retroflex", ">": "voiced",
    "#": "aspirated", "<": "voiceless", "%": "not aspirated", "C": "consonant", "V": "vowel"
};
const wildcards = {"*": "0 or more characters", "|": "marks end of lemma"};

//show keyboard expand
function printValue (val) {
    document.getElementById('user-input').value += val;
};

var keyIds = []
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
        var specialCharsGreek = {"á": "1", "é": "2", "ē": "3", "ō": "4", "ḗ": "5", "ṓ": "6", "ý": "7", "í": "8"};
        var specialCharsVedic = {
            'á': "1", 'à': "2", 'ā': "3",'é': "4", 'è': "5", 'ì': "6", 'í': "6", 'ī': "7", 'ù': "8", 'ú': "9",
            'ṭ': "9", 'ṭh': "10", 'ḍ': "11", 'ḍh': "12", 'ṃ': "13",'ṇ': "14", 'ṣ': "15", 'ś': "16"
        };
        greek = [featuresGreek, specialCharsGreek, wildcards];
        vedic = [featuresVedic, specialCharsVedic, wildcards];

        for (var count=0; count<=1; count++) {
            var kind;
            if (language === "1") {
                kind = greek[count];
            } else if (language === "2") {
                kind = vedic[count];
            }
            innerContainer = document.createElement("div");
            innerContainer.setAttribute("class", "inner-key-container");
            //console.log(kind);
            for (var [key, value] of Object.entries(kind)) {
                //var spanKey = document.createElement("span");
                //spanKey.setAttribute("class", "key-span");
                var btnKey = document.createElement("button");
                btnKey.innerText = key;
                btnKey.setAttribute("class", "key");
                btnKey.setAttribute("value", key);
                btnKey.setAttribute("onclick", "printValue(this.value);");
                keyIds.push(`key${key}`);
                btnKey.setAttribute("id", `key${key}`);
                //spanKey.append(btnKey);
                innerContainer.append(btnKey);
                //innerContainer.append(spanKey);
                //keyboardContainer.append(spanKey);
                //btnKey.addEventListener("click" try with EventListener
            }
            keyboardContainer.append(innerContainer);
        }
        document.getElementById("expand-keyboard-section").append(keyboardContainer);
    }
});
