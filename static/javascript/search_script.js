/*
================================================================================================ 
Dictionaries
*/

const featuresGreek = {
    "A": "alveolar", "L": "labial", "K": "velar", "J": "palatal",
    "P": "plosive", "Z": "affricate", "R": "approximant", "N": "nasal", "F": "fricative", ">": "voiced",
    "#": "aspirated", "<": "voiceless", "%": "not aspirated", "C": "consonant", "V": "vowel"
};

const featuresVedic = {
    "A": "alveolar", "L": "labial", "K": "velar", "J": "palatal",
    "P": "plosive", "R": "approximant", "W": "sonorant", "N": "nasal", "F": "fricative", "H": "laryngeal", "X": "retroflex", ">": "voiced",
    "#": "aspirated", "<": "voiceless", "%": "not aspirated", "C": "consonant", "V": "vowel"
};

const featuresLatin = {
    "A": "alveolar", "L": "labial", "K": "velar", "J": "palatal",
    "P": "plosive", "Z": "affricate", "R": "approximant", "N": "nasal", "F": "fricative", "H": "laryngeal", ">": "voiced",
    "#": "aspirated", "<": "voiceless", "%": "not aspirated", "C": "consonant", "V": "vowel"
};

const featuresArmenian = {
    "A": "alveolar", "L": "labial", "K": "velar", "J": "palatal", "O": "postalveolar", "X": "lateral", "Q": "trill", "R": "flap",
    "W": "glide", "P": "plosive", "Z": "affricate", "N": "nasal", "F": "fricative", "H": "laryngeal", ">": "voiced",
    "#": "aspirated", "<": "voiceless", "%": "not aspirated", "C": "consonant", "V": "vowel"
}

const wildcards = {"*": "0 or more characters", "|": "marks end of lemma"};


/*
================================================================================================ 
INITIAL CALLS
*/

renderKey();
generateKeyboard(language = "1");


/*
================================================================================================ 
EVENT-LISTENERS
*/

document.getElementById("user-input").addEventListener("keypress", key => {
    var existing = document.getElementById("add-input-field");
    if (existing != null) {
        document.getElementById("add-input-field").setAttribute("class", "text-field");
    }
    wrongInputHandling(key, key.key, "user-input");
});

var chooseDropdown = document.getElementById("choose-language-id");
// render key by change
chooseDropdown.addEventListener("change", () => {
    console.log("change key")
    const oldContainer = document.getElementById("key-container");
    if (oldContainer) {
        console.log("key container exists")
        oldContainer.remove();
    };
    renderKey();
});

// generate keyboard by change
chooseDropdown.addEventListener("change", () => {
    var language = document.getElementById("choose-language-id").value;
    const oldContainer = document.getElementById("keyboard-container");
    if (oldContainer) {
        console.log("keyboard container exists")
        oldContainer.remove();
    };

    generateKeyboard(language);
});

// removes value of input fields by change of language
chooseDropdown.addEventListener("change", () => {
    const userInput = document.getElementById("user-input");
    const addInput = document.getElementById("add-input-field");
    userInput.value = "";
    addInput.value = "";
});


//event listener for add phoneme button
//adds secondary input field remove button and add button and their event listeners
document.getElementById("plus-button").addEventListener("click", () => {
    var addContainer = document.createElement("div");
    var addInput = document.createElement("input");
    var addBtn = document.createElement("button");
    var delBtn = document.createElement("button");

    addContainer.setAttribute("id", "add-phoneme-container");
    addContainer.setAttribute("class", "form-part-container");
    addInput.setAttribute("class", "text-field");
    addInput.setAttribute("id", "add-input-field");
    addInput.setAttribute("placeholder", "search pattern");
    addBtn.setAttribute("type", "button");
    addBtn.setAttribute("id", "add-button");
    addBtn.textContent = "add";
    delBtn.setAttribute("type", "button");
    delBtn.setAttribute("id", "minus-button");
    delBtn.setAttribute("class", "plus-minus-button");
    delBtn.textContent = "-";

    addContainer.append(delBtn, addInput, addBtn);
    document.getElementById("search-form").append(addContainer);


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


/*
================================================================================================ 
Functions
*/

// renders HTML for key tables
function renderKey () {
    var language = document.getElementById("choose-language-id").value;
    const oldContainer = document.getElementById("key-container");
    if (oldContainer) {
        console.log("key container exists")
        oldContainer.remove();
    };
    const section = document.getElementById("key-section");
    const keyContainer = document.createElement("div");
    keyContainer.setAttribute("id", "key-container");
    section.append(keyContainer);
    console.log(language);
    if (language === "1") {
        
        keyContainer.innerHTML =
            `<table class="key-con-table">
                <tr>
                    <th class="head-roll"><span class="feature">Greek</span></th>
                    <th><span class="feature">labial<span><div class="user-key">key: L</div></th>
                    <th><span class="feature">alveolar</span><div class="user-key">key: A</div></th>
                    <th><span class="feature">velar</span><div class="user-key">key: K</div></th>
                </tr>
                <tr>
                    <td class="phoneme-category"><span class="feature">plosives</span><div class="user-key">key: P</div></td>
                </tr>
                <tr>
                    <td><span class="feature">-voice</span><div class="user-key">key: P+&lt;</div></td>
                    <td>p</td>
                    <td>t</td>
                    <td>k</td>
                </tr>
                <tr>
                    <td><span class="feature">+voice</span><div class="user-key">key: P+&gt;</div></td>
                    <td>b</td>
                    <td>d</td>
                    <td>g</td>
                </tr>
                <tr>
                    <td><span class="feature">+aspirate</span><div class="user-key">key: P+#</div></td>
                    <td>ph</td>
                    <td>th</td>
                    <td>kh</td>
                </tr>
                <tr><td class="phoneme-category"><span class="feature">affricate</span><div class="user-key">key: Z</div></td></tr>
                <tr>
                    <td></td>
                    <td>ps</td>
                    <td>z</td>
                    <td>ks</td>
                </tr>
                <tr><td class="phoneme-category"><span class="feature">non plosives</span></td></tr>
                <tr>
                    <td><span class="feature">nasal</span><div class="user-key">key: N</div></td>
                    <td>m</td>
                    <td>n</td>
                    <td></td>
                </tr>
                <tr>
                    <td><span class="feature">approximant</span><div class="user-key">key: R</div></td>
                    <td></td>
                    <td>l r</td>
                    <td></td>
                </tr>
                <tr>
                    <td><span class="feature">fricative</span><div class="user-key">key: F</div></td>
                    <td></td>
                    <td>s</td>
                    <td></td>
                </tr>
            </table>
            <table class="key-vow-table">
                <tr>
                    <th></th>
                    <th>front</th>
                    <th>mid</th>
                    <th>back</th>
                </tr>
                <tr>
                    <td>high</td>
                    <td>i í, y ý</td>
                    <td></td>
                    <td>u ú</td>
                </tr>
                <tr>
                    <td></td>
                    <td>e é, ē ḗ</td>
                    <td></td>
                    <td>o ó, ō ṓ</td>
                </tr>
                <tr>
                    <td>low</td>
                    <td></td>
                    <td>a á</td>
                    <td></td>
                </tr>
            </table>`;
    } else if (language === "2") {
        keyContainer.innerHTML = 
        `<table class="key-con-table">
        <tr>
            <th><span class="feature">Vedic</span></th>
            <th>labial</th>
            <th>alveolar</th>
            <th>retroflex</th>
            <th>palatal</th>
            <th>velar</th>
        </tr>
        <tr>
        <td class="phoneme-category"><span class="feature">plosives</span><div class="user-key">key: P</div></td>
        <td class="user-key">key: L</td>
        <td class="user-key">key: A</td>
        <td class="user-key">key: X</td>
        <td class="user-key">key: J</td>
        <td class="user-key">key: K</td>
        </tr>
        <tr>
            <td><span class="feature">-voice -aspirate</span><div class="user-key">key: P+&lt;+%</div></td>
            <td>p</td>
            <td>t</td>
            <td>ṭ</td>
            <td></td>
            <td>k</td>
        </tr>
        <tr>
            <td><span class="feature">-voice +aspirate</span><div class="user-key">key: P+&lt;+#</div></td>
            <td>ph</td>
            <td>th</td>
            <td>ṭh</td>
            <td></td>
            <td>kh</td>
        </tr>
        <tr>
            <td><span class="feature">+voice -aspirate</span><div class="user-key">key: P+&gt;+%</div></td>
            <td>b</td>
            <td>d</td>
            <td>ḍ</td>
            <td></td>
            <td>g</td>
        </tr>
        <tr>
            <td><span class="feature">+voice +aspirate</span><div class="user-key">key: P+&gt;+#</div></td>
            <td>bh</td>
            <td>dh</td>
            <td>ḍh</td>
            <td></td>
            <td>gh</td>
        </tr>
        <tr>
            <td class="phoneme-category"><span class="feature">affricates</span><div class="user-key">key: Z</div></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><span class="feature">-voice -aspirate</span></td>
            <td></td>
            <td></td>
            <td></td>
            <td>c</td>
            <td></td>
        </tr>
        <tr>
            <td><span class="feature">-voice +aspirate</span></td>
            <td></td>
            <td></td>
            <td></td>
            <td>ch</td>
            <td></td>
        </tr>
        <tr>
            <td><span class="feature">+voice -aspirate</span></td>
            <td></td>
            <td></td>
            <td></td>
            <td>j</td>
            <td></td>
        </tr>
        <tr>
            <td class="phoneme-category"><span class="feature">non plosives</span></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><span class="feature">glide</span><div class="user-key">key: W</div></td>
            <td>v</td>
            <td></td>
            <td></td>
            <td>y</td>
            <td></td>
        </tr>
        <tr>
            <td><span class="feature">nasal</span><div class="user-key">key: N</div></td>
            <td>m</td>
            <td>n</td>
            <td>ṇ</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><span class="feature">approximant</span><div class="user-key">key: R</div></td>
            <td></td>
            <td>l r</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><span class="feature">fricative</span><div class="user-key">key: W</div></td>
            <td></td>
            <td>s</td>
            <td>ṣ</td>
            <td>ś</td>
            <td></td>
        </tr>
    </table>`;
    } else if (language === "3") {
        keyContainer.innerHTML = 
    `<table class="key-con-table">
        <tr>
            <th class="head-roll"><span class="feature">Latin</span></th>
            <th><span class="feature">labial<span><div class="user-key">key: L</div></th>
            <th><span class="feature">alveolar</span><div class="user-key">key: A</div></th>
            <th><span class="feature">velar</span><div class="user-key">key: K</div></th>
            <th><span class="feature">labiovelar</span><div class="user-key">key: Q</div></th>
            <th><span class="feature">laryngeal</span><div class="user-key">key: H</div></th>
        </tr>
        <tr>
            <td class="phoneme-category"><span class="feature">plosives</span><div class="user-key">key: P</div></td>
        </tr>
        <tr>
            <td><span class="feature">-voice</span><div class="user-key">key: P+&lt;</div></td>
            <td>p</td>
            <td>t</td>
            <td>k</td>
            <td>qu</td>
            <td></td>
        </tr>
        <tr>
            <td><span class="feature">+voice</span><div class="user-key">key: P+&gt;</div></td>
            <td>b</td>
            <td>d</td>
            <td>g</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td class="phoneme-category"><span class="feature">non plosives</span></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><span class="feature">nasal</span><div class="user-key">key: N</div></td>
            <td>m</td>
            <td>n</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><span class="feature">approximant</span><div class="user-key">key: R</div></td>
            <td></td>
            <td>l r</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td><span class="feature">fricative</span><div class="user-key">key: F</div></td>
            <td>f</td>
            <td>s</td>
            <td></td>
            <td></td>
            <td>h</td>
        </tr>
    </table>`
    } else if (language === "4") {
        keyContainer.innerHTML = `coming soon`
    };
};


// if key of virtual keyboard is pressed key is added to search input
function printValue (val) {
    document.getElementById('user-input').value += val;
};
// generates keyboard containing keys for key-characters and special characters in the respective language
function generateKeyboard(language) {
    console.log(language)
    var keyIds = []
    var keyboardContainer = document.createElement("div");
    keyboardContainer.setAttribute("id", "keyboard-container");
    keyboardContainer.setAttribute("class", "expand-container");
    //var language = document.getElementById("choose-language-id").value;
    var specialCharsGreek = {"á": "1", "é": "2", "ē": "3", "ō": "4", "ḗ": "5", "ṓ": "6", "ý": "7", "í": "8"};
    var specialCharsVedic = {
        'á': "1", 'à': "2", 'ā': "3",'é': "4", 'è': "5", 'ì': "6", 'í': "6", 'ī': "7", 'ù': "8", 'ú': "9",
        'ṭ': "9", 'ṭh': "10", 'ḍ': "11", 'ḍh': "12", 'ṃ': "13",'ṇ': "14", 'ṣ': "15", 'ś': "16"
    };
    var specialCharsArmenian = {
        'ē': "1", 'ǝ': "2", 'š': "3", 'ž': "4", 'ł': "5", 'č': "6", 'ǰ': "7", "ṙ": "8"
    };

    noChars = null;

    greek = [featuresGreek, specialCharsGreek, wildcards];
    vedic = [featuresVedic, specialCharsVedic, wildcards];
    latin = [featuresLatin, noChars, wildcards];
    armenian = [featuresArmenian, specialCharsArmenian, wildcards]

    for (var count=0; count<=1; count++) {
        var kind;
        if (language === "1") {
            kind = greek[count];
        } else if (language === "2") {
            kind = vedic[count];
        } else if (language === "3") {
            kind = latin[count];
        } else if (language === "4") {
            kind = armenian[count];
        };

        if (kind == null) {
            console.log("null");
            continue;
        };

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
            innerContainer.append(btnKey);
        }
        keyboardContainer.append(innerContainer);
    }
    document.getElementById("expand-keyboard-section").append(keyboardContainer);
};


function removeDisabled(id) {
    document.getElementById(id).removeAttribute("disabled");
}
// adds content of add phoneme input field to main input field
function addToSearch(inputContent) {
    const searchInput = document.getElementById("user-input");
    searchInput.value += inputContent;
    document.getElementById("add-phoneme-container").remove();
    removeDisabled("plus-button");
}


// adds a message for user if input is not allowed
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


// handles input in the main and secondary input field
// checks whether given char is in list of allowed inputs of the respective language
// special treatment for h in Greek which is only allowed after certain characters
function wrongInputHandling(key, pressed, fieldId) {
    if (document.getElementById("wrong-message-id")) {
        document.getElementById("wrong-message-id").remove();
        document.getElementById(fieldId).setAttribute("class", "text-field");
    }
    var allowed;

    const greekAllowed = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', 'A', 'C', 'F', 'J', 'K', 'L', 'N', 'P',
                          'R', 'V', 'Z', '|', 'y', 'a', 'e', 'ē', 'y', 'o', 'ō', 'i', 'a', 'o', 'ō', 'i', 'u',
                          'u', 'p', 'b', 'ph', 't', 'd', 'th', 'k', 'g', 'kh', 'ks', 'z', 'm', 'n', 'l', 'r', 's', 's',
                          'ps', 'h', 'Enter'
                        ];
    const vedicAllowed = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', 'A', 'C', 'F', 'H', 'J', 'K', 'L', 'N', 'P',
                          'R', 'V', 'W', 'X', 'Z', '|', 'a', 'á', 'à', 'ā', "e", 'é', 'è', 'i', 'ì', 'í', 'ī', 'o', 'ò', 'u',
                          'ù', 'ú', 'p', 'ph', 'b', 'bh', 't', 'th', 'd', 'dh', 'ṭ', 'ṭh', 'ḍ', 'ḍh', 'k', 'kh', 'g',
                          'gh', 'c', 'ch', 'j', 'v', 'y', 'm', 'ṃ', 'n', 'ṇ', 'l', 'r', 's', 'ṣ', 'ś', 'h', 'Enter'
                        ];
    
    const latinAllowed = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', '|','A', 'C', 'F', 'J', 'K', 'L', 'N', 'P',
                          'R', 'V', 'H', 'Q', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'm', 'n', 'o', 'p',
                          'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z', 'Enter'
                        ];

    const armenianAllowed = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', '|','A', 'C', 'F', 'J', 'K', 'L', 'N', 'P',
                             'R', 'V', 'H', 'Q', 'Z', "'", 'a', 'e', 'ē', 'ǝ', 'i', 'o', 'u',
                             'p', 'b', 't', 'd', 'ṭ', 'ḍ', 'k', 'g', 'c', 'j', 'v', 'y', 'm', 'n', 'l', 'r', 'ṙ', 's', 'h', 'š',
                             'ž', 'ł', 'č', 'ǰ', 'f', 'Enter'
                            ];

    const greekFollows = {"h": ["p", "t", "k"]};
    const greekInitial = ["h"];
    const armenianFollows = {"'": ["p", "t", "k", "c", "č"], "h": ["p"]};
    var follows;
    var initial;

    var language = document.getElementById("choose-language-id").value;
    console.log(language);
    if (language === "1") {
        allowed = greekAllowed;
        follows = greekFollows;
        initial = greekInitial;
        lang = "Greek";
    } else if (language === "2") {
        allowed = vedicAllowed;
        follows = {"": ""};
        initial = [""]
        lang = "Vedic";
    } else if (language === "3") {
        allowed = latinAllowed;
        follows = {"": ""};
        initial = [""];
        lang = "Latin";
    } else if (language === "4") {
        allowed = armenianAllowed;
        follows = armenianFollows;
        initial = [""];
        lang = "Armenian";
    };
    
    if (allowed.includes(pressed)) {
        if (follows.hasOwnProperty(pressed)) {
            fieldValue = document.getElementById(fieldId).value;
            lastChar = fieldValue.slice(-1);
            var value = follows[pressed];
            if (value.includes(lastChar)) {
                console.log("allowed input");
            } else {
                var message = `'${pressed}' only allowed after ${value.join(", ")}`;
                key.preventDefault();
                wrongInput(message, fieldId);
            };
        };
    } else {
        var message = `character '${pressed}' is no allowed input for ${lang}`;
        key.preventDefault();
        wrongInput(message, fieldId);
    }
}


/*const phonemesGreek = {
    "a": " α", "e": " ε", "ē": " η", "i": " ι", "o": " ο", "ō": " ω", "y": " υ", "u": " ου", "a": " ά", "é": " έ",
    "i": " ί", "o": " ό", "ō": " ώ", "y": " ύ", "u": " όυ", "ē": " ή", "i": " ι", "p": " π", "b": " β", "ph": "φ",
    "t": " τ", "d": " δ", "th": "θ", "k": " κ", "g": " γ", "kh": "χ", "z": " ζ", "m": " μ", "n": " ν", "l": " λ",
    "r": " ρ", "s": " σ", "s": " ς", "ps": "ψ", "p": " π", "b": " β", "ph": "φ", "t": " τ", "d": " δ", "th": "θ",
    "k": " κ", "g": " γ", "ks": "ξ"
};

if (language == "1") {
            if (pressed == "h") {
                fieldValue = document.getElementById(fieldId).value;
                lastChar = fieldValue.slice(-1);
                if ((lastChar != "p") && (lastChar != "k") && (lastChar != "t") && fieldValue.length != 0) {
                    var message = `'h' only allowed after 'p', 'k', 't' or as first character`;
                    key.preventDefault();
                    wrongInput(message, fieldId);
                }
            }

*/