/*
================================================================================================ 
DATA
*/

function getLanguage () {
    language = document.getElementById("choose-language-id").value;
    return language;
};

language = getLanguage();


const featuresGreek = {
    "B": "labial", "A": "alveolar", "K": "velar",
    "N": "nasal", "P": "plosive", "Z": "affricate", "F": "fricative", "R": "rhotic",
    "C": "consonant", "V": "vowel",
    ">": "voiced", "#": "aspirated", "<": "voiceless", "%": "not aspirated"
};

const featuresVedic = {
    "B": "labial", "D": "labiodental", "A": "alveolar", "X": "retroflex",  "J": "palatal", "K": "velar", "H": "glottal",
    "N": "nasal", "P": "plosive", "F": "fricative", "W": "glide", "R": "rhotic", "L": "lateral",
    "C": "consonant", "V": "vowel",
    ">": "voiced", "#": "aspirated", "<": "voiceless", "%": "not aspirated"
};

const featuresLatin = {
    "B": "labial", "D": "labiodental", "Q": "labiovelar", "A": "alveolar", "J": "palatal", "K": "velar", "H": "glottal",
    "N": "nasal", "P": "plosive", "Z": "affricate", "F": "fricative", "W": "glide", "R": "rhotic",
    "C": "consonant", "V": "vowel",
    ">": "voiced", "#": "aspirated", "<": "voiceless", "%": "not aspirated"
};

const featuresArmenian = {
    "B": "labial", "D": "labiodental", "A": "alveolar", "S": "postalveolar", "J": "palatal", "K": "velar", "H": "glottal",
    "N": "nasal", "P": "plosive", "Z": "affricate", "F": "fricative", "W": "glide", "R": "trill", "ɾ": "flap", "L": "lateral",
    "C": "consonant", "V": "vowel",
    ">": "voiced", "#": "aspirated", "<": "voiceless", "%": "not aspirated"
}

const wildcards = {"*": "0 or more characters", "|": "marks end of lemma"};


// input validation

const greekAllowed = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', 'A', 'C', 'F', 'J', 'K', 'L', 'N', 'P', 'B',
'R', 'V', 'Z', '|', 'y', 'a', 'e', 'ē', 'y', 'o', 'ō', 'i', 'a', 'o', 'ō', 'i', 'u', 'é', 'á', 'ḗ', 'ṓ',' ý', 'í',
'p', 'b', 'ph', 't', 'd', 'th', 'k', 'g', 'kh', 'ks', 'z', 'm', 'n', 'l', 'r', 's',
'ps', 'h', 'Enter'
];
const vedicAllowed = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', 'A', 'C', 'F', 'H', 'J', 'K', 'L', 'N', 'P',
'R', 'V', 'W', 'X', 'Z', '|', 'a', 'á', 'à', 'ā', "e", 'é', 'è', 'i', 'ì', 'í', 'ī', 'o', 'ò', 'u',
'ù', 'ú', 'ū', 'p', 'ph', 'b', 'bh', 't', 'th', 'd', 'dh', 'ṭ', 'ṭh', 'ḍ', 'ḍh', 'k', 'kh', 'g',
'gh', 'c', 'ch', 'j', 'v', 'y', 'm', 'ṃ', 'n', 'ṇ', 'l', 'r', 's', 'ṣ', 'ś', 'h', "ñ", "ṅ", "m̐", 'ḥ', 'Enter'
];

const latinAllowed = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', '|','A', 'C', 'F', 'J', 'K', 'L', 'N', 'P',
'R', 'V', 'H', 'Q', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'm', 'n', 'o', 'p',
'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z', 'Enter'
];

const armenianAllowed = ['(', ')', '+', '#', '%', '(', ')', '*', '<', '>', '|','A', 'C', 'F', 'J', 'K', 'L', 'N', 'P',
   'R', 'V', 'H', 'Q', 'Z', "`", 'a', 'e', 'ē', 'ǝ', 'i', 'o', 'u',
   'p', 'b', 't', 'd', 'ṭ', 'ḍ', 'k', 'g', 'c', 'j', 'v', 'y', 'm', 'n', 'l', 'r', 'ṙ', 's', 'h', 'š',
   'ž', 'ł', 'č', 'ǰ', 'f', 'Enter'
];

const greekFollows = {"h": ["p", "t", "k"]};
const greekInitial = ["h"];
const armenianFollows = {"`": ["p", "t", "k", "c", "č"]};

// key-table generating

const placeCon = {"B": "labial", "D": "labiodental", "Q": "labiovelar", "A": "alveolar", "S": "postalveolar", "X": "retroflex", "J": "palatal", "K": "velar", "H": "glottal"};
if (language === "4") {
    var manner = {"N": "nasal", "P": "plosive", "Z": "affricate", "F": "fricative", "W": "glide", "R": "trill", "ɾ": "flap", "L": "lateral"};
} else {
    var manner = {"N": "nasal", "P": "plosive", "Z": "affricate", "F": "fricative", "W": "glide", "R": "rhotic", "L": "lateral"};
}

const placeVow = ['front', 'mid', 'back'];
const pitch = ['high', '', 'low'];

const greekVow = {'y': ['high', 'front'], 'a': ['low', 'mid'], 'e': ['', 'front'], 'ē': ['', 'front'], 'o': ['', 'back'], 'ō': ['', 'back'], 'i': ['high', 'front'], 'u': ['high', 'back']}
const greekCon = {
                'p': ['plosive', 'labial', 'voiceless', 'notAsp'],
                'b': ['plosive', 'labial', 'voice', 'notAsp'],
                'ph': ['plosive', 'labial', 'voiceless', 'asp'],
                't': ['plosive', 'alveolar', 'voiceless', 'notAsp'],
                'd': ['plosive', 'alveolar', 'voice', 'notAsp'],
                'th': ['plosive', 'alveolar', 'voiceless', 'asp'],
                'k': ['plosive', 'velar', 'voiceless', 'notAsp'],
                'g': ['plosive', 'velar', 'voice', 'notAsp'],
                'kh': ['plosive', 'velar', 'voiceless', 'asp'],
                'ks': ['affricate', 'velar', 'voiceless', 'notAsp'],
                'z': ['affricate', 'alveolar', 'voiceless', 'notAsp'],
                'n': ['nasal', 'alveolar', 'voice', 'notAsp'],
                'm': ['nasal', 'labial', 'voice', 'notAsp'],
                'l': ['lateral', 'alveolar', 'voiceless', 'notAsp'],
                'r': ['rhotic', 'alveolar', 'voiceless', 'notAsp'],
                's': ['fricative', 'alveolar', 'voiceless', 'notAsp'],
                'ps': ['affricate', 'labial', 'voiceless', 'notAsp'],
                'h': ['fricative', 'glottal', 'voiceless', 'notAsp']
           };

const vedicVow = {'a': ['low', 'mid'], 'á': ['low', 'mid'], 'à': ['low', 'mid'], 'ā': ['low', 'mid'], 'e': ['', 'front'], 'é': ['', 'front'],
                    'è': ['', 'front'], 'i': ['high', 'front'], 'ì': ['high', 'front'], 'í': ['high', 'front'], 'ī': ['high', 'front'], 'o': ['', 'back'],
                    'ò': ['', 'back'], 'u': ['high', 'back'], 'ù': ['high', 'back'], 'ú': ['high', 'back']
                };
const vedicCon = {
                'p': ['plosive', 'labial', 'voiceless', 'notAsp'],
                'b': ['plosive', 'labial', 'voice', 'notAsp'],
                'ph': ['plosive', 'labial', 'voiceless', 'asp'],
                'bh': ['plosive', 'labial', 'voice', 'asp'],
                't': ['plosive', 'alveolar', 'voiceless', 'notAsp'],
                'd': ['plosive', 'alveolar', 'voice', 'notAsp'],
                'th': ['plosive', 'alveolar', 'voiceless', 'asp'],
                'dh': ['plosive', 'alveolar', 'voice', 'asp'],
                'ṭ': ['plosive', 'retroflex', 'voiceless', 'notAsp'],
                'ṭh': ['plosive', 'retroflex', 'voiceless', 'asp'],
                'ḍ': ['plosive', 'retroflex', 'voice', 'notAsp'],
                'ḍh': ['plosive', 'retroflex', 'voice', 'asp'],
                'k': ['plosive', 'velar', 'voiceless', 'notAsp'],
                'g': ['plosive', 'velar', 'voice', 'notAsp'],
                'kh': ['plosive', 'velar', 'voiceless', 'asp'],
                'gh': ['plosive', 'velar', 'voice', 'asp'],
                'c': ['affricate', 'palatal', 'voiceless', 'notAsp'],
                'ch': ['affricate', 'palatal', 'voiceless', 'asp'],
                'j': ['affricate', 'palatal', 'voice', 'notAsp'],
                'v': ["glide", "labiodental", 'voice', 'notAsp'],
                'y': ["glide", "palatal", 'voice', 'notAsp'],
                'm': ['nasal', 'labial', 'voice', 'notAsp'], 
                'n': ['nasal', 'alveolar', 'voice', 'notAsp'],
                'ṇ': ['nasal', 'retroflex', 'voice', 'notAsp'],
                "ñ": ['nasal', 'palatal', 'voice', 'notAsp'],
                "ṅ": ['nasal', 'velar', 'voice', 'notAsp'],
                'l': ['lateral', 'alveolar', 'voiceless', 'notAsp'],
                'r': ['rhotic', 'alveolar', 'voiceless', 'notAsp'],
                's': ['fricative', 'alveolar', 'voiceless', 'notAsp'],
                'ṣ': ['fricative', 'retroflex', 'voiceless', 'notAsp'],
                'ś': ['fricative', 'palatal', 'voiceless', 'notAsp'],
                'h': ['fricative', 'glottal', 'voiceless', 'notAsp']
};

const latinVow = {};
const latinCon = {
                'p': ['plosive', 'labial', 'voiceless', 'notAsp'],
                'b': ['plosive', 'labial', 'voice', 'notAsp'],
                'qu': ['plosive', 'labiovelar', 'voice', 'notAsp'],
                't': ['plosive', 'alveolar', 'voiceless', 'notAsp'],
                'd': ['plosive', 'alveolar', 'voice', 'notAsp'],
                'k': ['plosive', 'velar', 'voiceless', 'notAsp'],
                'g': ['plosive', 'velar', 'voice', 'notAsp'],
                'v': ["glide", "labiodental", 'voice', 'notAsp'],
                'm': ['nasal', 'labial', 'voice', 'notAsp'], 
                'n': ['nasal', 'alveolar', 'voice', 'notAsp'],
                'l': ['lateral', 'alveolar', 'voiceless', 'notAsp'],
                'r': ['rhotic', 'alveolar', 'voiceless', 'notAsp'],
                's': ['fricative', 'alveolar', 'voiceless', 'notAsp'],
                'f': ['fricative', 'labiodental', 'voiceless', 'notAsp'],
                'x': ["affricate", 'velar', 'voiceless', 'notAsp'],
                'h': ['fricative', 'glottal', 'voiceless', 'notAsp']
};

const armenianVow = {};
const armenianCon = {
                'p': ['plosive', 'labial', 'voiceless', 'notAsp'],
                'b': ['plosive', 'labial', 'voice', 'notAsp'],
                'p`': ['plosive', 'labial', 'voiceless', 'asp'],
                't': ['plosive', 'alveolar', 'voiceless', 'notAsp'],
                'd': ['plosive', 'alveolar', 'voice', 'notAsp'],
                't`': ['plosive', 'alveolar', 'voiceless', 'asp'],
                'k': ['plosive', 'velar', 'voiceless', 'notAsp'],
                'g': ['plosive', 'velar', 'voice', 'notAsp'],
                'k`': ['plosive', 'velar', 'voiceless', 'asp'],
                'n': ['nasal', 'labial', 'voice', 'notAsp'],
                'm': ['nasal', 'alveolar', 'voice', 'notAsp'],
                'l': ['lateral', 'alveolar', 'voiceless', 'notAsp'],
                'r': ['flap', 'alveolar', 'voiceless', 'notAsp'],
                'ṙ': ['trill', 'alveolar', 'voiceless', 'notAsp'],
                's': ['fricative', 'alveolar', 'voiceless', 'notAsp'],
                'n': ['nasal', 'alveolar', 'voice', 'notAsp'],
                'm': ['nasal', 'labial', 'voice', 'notAsp'],
                'v': ["glide", "labiodental", 'voice', 'notAsp'],
                'w': ["glide", "labiodental", 'voice', 'notAsp'],
                'y': ["glide", "palatal", 'voice', 'notAsp'],
                'l': ['lateral', 'alveolar', 'voiceless', 'notAsp'],
                'ł': ['lateral', 'velar', 'voiceless', 'notAsp'],
                'š': ['fricative', 'postalveolar', 'voiceless', 'notAsp'],
                'ž': ['fricative', 'postalveolar', 'voice', 'notAsp'],
                'x': ['fricative', 'velar', 'voiceless', 'notAsp'],
                'f': ['fricative', 'labiodental', 'voiceless', 'notAsp'],
                'c': ['affricate', 'alveolar', 'voiceless', 'notAsp'],
                'j': ['affricate', 'alveolar', 'voice', 'notAsp'],
                'c`': ['affricate', 'alveolar', 'voiceless', 'asp'],
                'č': ['affricate', 'postalveolar', 'voiceless', 'notAsp'],
                'ǰ': ['affricate', 'postalveolar', 'voice', 'notAsp'],
                'č`': ['affricate', 'postalveolar', 'voiceless', 'asp'],
                'h': ['fricative', 'glottal', 'voiceless', 'notAsp']
};

const cons = [greekCon, vedicCon, latinCon, armenianCon];
const vows = [greekVow, vedicVow, latinVow, armenianVow];

// keyboard generating
/** 
 * @specialCharsGreek 
 */
var specialCharsGreek = {
    "á": "1", "é": "2", "ē": "3", "ō": "4", "ḗ": "5", "ṓ": "6", "ý": "7", "í": "8"
};

var specialCharsVedic = {
    'á': "1", 'à': "2", 'ā': "3",'é': "4", 'è': "5", 'í': "6", 'ì': '7', 'ī': '8', 'ù': "9", 'ú': "10", 'ū': '11',
    'ṭ': "12", 'ḍ': "13", 's': '14', 'ś': "15", 'ṣ': "16", 'ṇ': "17", "ṅ": "18", "ñ": "19", "ḥ": "20", 'ṃ': "21", "m̐": "22"
};

var specialCharsArmenian = {
    'ē': "1", 'ǝ': "2", 'š': "3", 'ž': "4", 'ł': "5", 'č': "6", 'ǰ': "7", "ṙ": "8", "`": "9"
};


/*
================================================================================================ 
INITIAL CALLS
*/

renderKeyCon();
renderKeyVow();
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

const chooseDropdown = document.getElementById("choose-language-id");
// render key by change
chooseDropdown.addEventListener("change", () => {
    console.log("change key")
    const formerCon = document.getElementById("con-body");
    const formerVow = document.getElementById("vow-body");
    //if (formerCon) {
        console.log("key container exists")
        formerCon.remove();
        formerVow.remove();
    //};
    renderKeyCon();
    renderKeyVow();
});

// generate keyboard by change
chooseDropdown.addEventListener("change", () => {
    const formerKeyboard = document.getElementById("keyboard-container");
    if (formerKeyboard) {
        console.log("keyboard container exists")
        formerKeyboard.remove();
    };
    generateKeyboard();
});

// removes value of input fields by change of language
chooseDropdown.addEventListener("change", () => {
    const userInput = document.getElementById("user-input");
    const addInput = document.getElementById("add-input-field");
    userInput.value = "";
    if (addInput) {
        addInput.value = "";
    };
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

function fillField (innerText, phoneme){
    if(innerText !== "") {
        innerText += ", ";    
    };
    
    return innerText += phoneme;
};


function renderKeyCon () {

    let language = getLanguage();

    const langCon = cons[parseInt(language)-1];

    tbody = document.createElement("tbody");
    tbody.setAttribute("id", "con-body");
    conTable = document.getElementById("con-table");

    for (var [man_key, man_value] of Object.entries(manner)) {
        //console.log(man_value);
        let tableRoll = document.createElement("tr");
        tableRoll.innerHTML = `<td><span class="manner">${man_value}</span><span class="user-key">${man_key}</span></td>`;

        for (var [placeKey, place] of Object.entries(placeCon)) {
            //console.log(place);
            var td_nv_na = document.createElement("td");
            var td_nv_a = document.createElement("td");
            var td_v_na = document.createElement("td");
            var td_v_a = document.createElement("td");
            td_nv_na.setAttribute("class", "phoneme");
            td_nv_a.setAttribute("class", "phoneme");
            td_v_na.setAttribute("class", "phoneme");
            td_v_a.setAttribute("class", "phoneme");
          
            for (var [con, feature] of Object.entries(langCon)){

                //console.log(con);
                if (feature.includes(man_value) && feature.includes(place) && feature.includes("voiceless") && feature.includes("notAsp")) {
                    td_nv_na.innerText = fillField(td_nv_na.innerText, con)
                 
                } else if (feature.includes(man_value) && feature.includes(place) && feature.includes("voiceless") && feature.includes("asp")) {
                    td_nv_a.innerText = fillField(td_nv_a.innerText, con);
                
                } else if (feature.includes(man_value) && feature.includes(place) && feature.includes("voice") && feature.includes("notAsp")) {
                    td_v_na.innerText = fillField(td_v_na.innerText, con);
                 
                } else if (feature.includes(man_value) && feature.includes(place) && feature.includes("voice") && feature.includes("asp")) {
                    td_v_a.innerText = fillField(td_v_a.innerText, con);
                
                };
          
            };
            tableRoll.append(td_nv_na);
            tableRoll.append(td_nv_a);
            tableRoll.append(td_v_na);
            tableRoll.append(td_v_a);
        };
        tbody.append(tableRoll);    
    };
    conTable.append(tbody);
};


function renderKeyVow() {

    let language = getLanguage();
    const langVow = vows[parseInt(language)-1];

    var vowtbody = document.createElement("tbody");
    vowtbody.setAttribute("id", "vow-body");
    vowTable = document.getElementById("vow-table");

    for (var i=0; i<pitch.length; i++) {
        
        pitch_value = pitch[i];
        //console.log(pitch_value);

        let tableRoll = document.createElement("tr");
        tableRoll.innerHTML = `<td><span class="pitch">${pitch_value}</span></td>`;

        for (var placei=0; placei<placeVow.length; placei++) {
            let place = placeVow[placei];
            console.log(placei);
            console.log(place);
            var td = document.createElement("td");
            td.setAttribute("class", "phoneme");
          
            for (var [vow, feature] of Object.entries(langVow)){
                //console.log(vow);
                if (feature.includes(pitch_value) && feature.includes(place)) {
                    td.innerText = fillField(td.innerText, vow);
                };
            };
            tableRoll.append(td);
        };
        vowtbody.append(tableRoll);    
    };
    vowTable.append(vowtbody);
};


// if key of virtual keyboard is pressed key is added to search input
function printValue (val) {
    document.getElementById('user-input').value += val;
};
// generates keyboard containing keys for key-characters and special characters in the respective language
function generateKeyboard() {
    console.log(language)
    var keyIds = []
    var keyboardContainer = document.createElement("div");
    keyboardContainer.setAttribute("id", "keyboard-container");
    keyboardContainer.setAttribute("class", "expand-container");
    //var language = document.getElementById("choose-language-id").value;


    let noChars = {};

    greek = [featuresGreek, specialCharsGreek, wildcards];
    vedic = [featuresVedic, specialCharsVedic, wildcards];
    latin = [featuresLatin, noChars, wildcards];
    armenian = [featuresArmenian, specialCharsArmenian, wildcards];

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

        innerContainer = document.createElement("div");
        innerContainer.setAttribute("class", "inner-key-container");

        for (var [key, value] of Object.entries(kind)) {
            var btnKey = document.createElement("button");
            btnKey.innerText = key;
            btnKey.setAttribute("class", "key");
            btnKey.setAttribute("value", key);
            btnKey.setAttribute("onclick", "printValue(this.value);");
            keyIds.push(`key${key}`);
            btnKey.setAttribute("id", `key${key}`);
            innerContainer.append(btnKey);
        }
        if (innerContainer.innerHTML) {
            keyboardContainer.append(innerContainer);
        };
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
        initial = [""];
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
            } else if (initial.includes(pressed) && fieldValue.length === 0) {
                console.log("allowed input");
            } else {
                var message = `'${pressed}' only allowed after ${value.join(", ")}`;
                if (initial.includes(pressed)) {
                    message = message + ` or as initial phoneme`
                };
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
