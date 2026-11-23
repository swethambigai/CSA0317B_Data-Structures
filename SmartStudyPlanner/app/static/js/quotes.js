/* =========================================================
   SMART STUDY PLANNER
   MOTIVATIONAL QUOTES
   ========================================================= */


/* =========================================================
   QUOTE DATABASE
   ========================================================= */

const quotes = {

    motivation: [

        "Small steps every day create big results.",

        "Your pace is perfect — just don't stop.",

        "You are learning, growing, and becoming stronger.",

        "Consistency turns effort into progress.",

        "One focused session is better than a day of worrying.",

        "Keep showing up for yourself."
    ],


    calming: [

        "Rest is also part of progress.",

        "You do not have to finish everything today.",

        "Take a breath. You are allowed to slow down.",

        "A calm mind learns better.",

        "Pause, breathe, and continue when you are ready.",

        "Your wellbeing matters as much as your productivity."
    ],


    confidence: [

        "You have handled difficult things before. You can handle this too.",

        "You know more today than you did yesterday.",

        "Trust the preparation you have already done.",

        "You are capable of learning difficult things.",

        "One question at a time. One topic at a time.",

        "You don't need perfection. You need progress."
    ],


    consistency: [

        "A little progress every day adds up.",

        "You don't need motivation every day. Build the habit.",

        "Show up today, even if it is only for a little while.",

        "Consistency beats intensity when building long-term skills.",

        "Keep the chain going.",

        "Your future self will thank you for today's effort."
    ]
};


/* =========================================================
   GET RANDOM QUOTE
   ========================================================= */

function getRandomQuote(category) {

    const selectedCategory =
        quotes[category]
            ? category
            : "motivation";


    const categoryQuotes =
        quotes[selectedCategory];


    const index =
        Math.floor(
            Math.random() *
            categoryQuotes.length
        );


    return categoryQuotes[index];
}


/* =========================================================
   DETERMINE QUOTE CATEGORY
   ========================================================= */

function getQuoteCategory(
    mood,
    fatigueScore,
    examMode
) {

    if (examMode === true) {

        return "confidence";
    }


    if (
        mood === "Stressed" ||
        fatigueScore > 15
    ) {

        return "calming";
    }


    if (
        mood === "Tired" ||
        fatigueScore > 10
    ) {

        return "calming";
    }


    if (mood === "Neutral") {

        return "consistency";
    }


    return "motivation";
}


/* =========================================================
   DISPLAY QUOTE
   ========================================================= */

function displayQuote(
    category
) {

    const quoteElement =
        document.getElementById("dailyQuote") ||
        document.getElementById("daily-quote");


    if (!quoteElement) {
        return;
    }


    const quote =
        getRandomQuote(category);


    quoteElement.textContent =
        "“" + quote + "”";
}


/* =========================================================
   DISPLAY QUOTE AUTOMATICALLY
   ========================================================= */

function initializeQuoteSystem() {

    const stored =
        localStorage.getItem(
            "smartStudyPlannerPlanner"
        );


    let mood =
        "Neutral";


    let fatigueScore =
        0;


    if (stored) {

        try {

            const data =
                JSON.parse(stored);


            if (
                data.plannerData
                &&
                data.plannerData.mood
            ) {

                mood =
                    data.plannerData.mood;
            }


            if (
                data.plannerData
                &&
                data.plannerData.fatigueScore
                !== undefined
            ) {

                fatigueScore =
                    Number(
                        data.plannerData.fatigueScore
                    );
            }

        } catch (error) {

            console.error(
                "Unable to load quote data:",
                error
            );
        }
    }


    const category =
        getQuoteCategory(
            mood,
            fatigueScore,
            false
        );


    displayQuote(category);
}


/* =========================================================
   QUOTE ON PAGE LOAD
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        initializeQuoteSystem();

        const newQuoteButton =
            document.getElementById("newQuoteBtn") ||
            document.getElementById("new-quote-btn");

        if (newQuoteButton) {
            newQuoteButton.addEventListener("click", changeQuote);
        }
    }
);


/* =========================================================
   CHANGE QUOTE
   ========================================================= */

function changeQuote() {

    const stored =
        localStorage.getItem(
            "smartStudyPlannerPlanner"
        );


    let mood =
        "Neutral";


    let fatigueScore =
        0;


    if (stored) {

        try {

            const data =
                JSON.parse(stored);


            mood =
                data.plannerData?.mood ||
                "Neutral";


            fatigueScore =
                Number(
                    data.plannerData
                        ?.fatigueScore || 0
                );

        } catch (error) {

            console.error(
                "Quote data error:",
                error
            );
        }
    }


    const category =
        getQuoteCategory(
            mood,
            fatigueScore,
            false
        );


    displayQuote(category);
}


/* =========================================================
   QUOTE BY MOOD
   ========================================================= */

function displayQuoteForMood(
    mood
) {

    const category =
        getQuoteCategory(
            mood,
            0,
            false
        );


    displayQuote(category);
}


/* =========================================================
   QUOTE BY FATIGUE
   ========================================================= */

function displayQuoteForFatigue(
    fatigueScore
) {

    const category =
        getQuoteCategory(
            "Neutral",
            Number(fatigueScore),
            false
        );


    displayQuote(category);
}


/* =========================================================
   PUBLIC FUNCTIONS
   ========================================================= */

window.getRandomQuote =
    getRandomQuote;

window.getQuoteCategory =
    getQuoteCategory;

window.displayQuote =
    displayQuote;

window.changeQuote =
    changeQuote;

window.displayQuoteForMood =
    displayQuoteForMood;

window.displayQuoteForFatigue =
    displayQuoteForFatigue;