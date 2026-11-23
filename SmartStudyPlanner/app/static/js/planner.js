/* =========================================================
   SMART STUDY PLANNER
   PLANNER JAVASCRIPT
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    initializePlanner();
});


/* =========================================================
   GLOBAL DATA
   ========================================================= */

let studyQueue = [];
let revisionStack = [];

let plannerData = {
    hoursStudied: 0,
    continuousSessions: 0,
    difficulty: 1,
    mood: "Neutral",
    sleepHours: 7,
    breaks: 0,
    fatigueScore: 0,
    fatigueLevel: "Normal"
};


/* =========================================================
   INITIALIZE
   ========================================================= */

function initializePlanner() {

    loadPlannerData();

    setupPlannerForm();

    setupFatigueInputs();

    updatePlannerDisplay();

    calculateAndDisplayFatigue();
}


/* =========================================================
   LOAD DATA
   ========================================================= */

function loadPlannerData() {

    const savedPlanner =
        localStorage.getItem(
            "smartStudyPlannerPlanner"
        );

    if (savedPlanner) {

        try {

            const saved =
                JSON.parse(savedPlanner);

            if (Array.isArray(saved.studyQueue)) {

                studyQueue =
                    saved.studyQueue;
            }

            if (Array.isArray(saved.revisionStack)) {

                revisionStack =
                    saved.revisionStack;
            }

            if (saved.plannerData) {

                plannerData =
                    {
                        ...plannerData,
                        ...saved.plannerData
                    };
            }

        } catch (error) {

            console.error(
                "Unable to load planner data:",
                error
            );
        }
    }
}


/* =========================================================
   SAVE DATA
   ========================================================= */

function savePlannerData() {

    const data = {

        studyQueue: studyQueue,

        revisionStack: revisionStack,

        plannerData: plannerData
    };


    localStorage.setItem(
        "smartStudyPlannerPlanner",
        JSON.stringify(data)
    );
}


/* =========================================================
   PLANNER FORM
   ========================================================= */

function setupPlannerForm() {

    const form =
        document.getElementById(
            "plannerForm"
        );

    if (!form) {
        return;
    }


    form.addEventListener(
        "submit",
        function (event) {

            event.preventDefault();

            addTopicFromForm();
        }
    );
}


/* =========================================================
   ADD TOPIC
   ========================================================= */

function addTopicFromForm() {

    const topicInput =
        document.getElementById("topic") ||
        document.getElementById("topicName");

    const subjectInput =
        document.getElementById("subject") ||
        document.getElementById("subjectName");

    const difficultyInput =
        document.getElementById("difficulty") ||
        document.getElementById("topicDifficulty");

    const durationInput =
        document.getElementById("duration") ||
        document.getElementById("topicDuration");


    if (!topicInput) {
        return;
    }


    const topicName =
        topicInput.value.trim();


    if (topicName === "") {

        alert(
            "Please enter a topic."
        );

        return;
    }


    const topic = {

        id: Date.now(),

        name: topicName,

        subject:
            subjectInput
                ? subjectInput.value.trim()
                : "General",

        difficulty:
            difficultyInput
                ? difficultyInput.value
                : "Medium",

        duration:
            durationInput
                ? Number(durationInput.value)
                : 30,

        completed: false,

        addedAt:
            new Date().toISOString()
    };


    studyQueue.push(topic);

    savePlannerData();

    updatePlannerDisplay();

    topicInput.value = "";
}


/* =========================================================
   DISPLAY QUEUE
   ========================================================= */

function updatePlannerDisplay() {

    const queueElement =
        document.getElementById(
            "studyQueue"
        );

    if (!queueElement) {
        return;
    }


    queueElement.innerHTML = "";


    if (studyQueue.length === 0) {

        queueElement.innerHTML = `
            <p class="empty-message">
                No topics in your study queue.
            </p>
        `;

        return;
    }


    studyQueue.forEach(
        function (topic, index) {

            const item =
                document.createElement("div");

            item.className =
                "topic-item";


            item.innerHTML = `

                <div class="topic-number">
                    ${index + 1}
                </div>

                <div class="topic-details">

                    <strong>
                        ${escapeHTML(topic.name)}
                    </strong>

                    <span>
                        ${escapeHTML(topic.subject)}
                        •
                        ${topic.duration} min
                    </span>

                </div>

                <span class="difficulty ${getDifficultyClass(topic.difficulty)}">
                    ${escapeHTML(topic.difficulty)}
                </span>

                <button
                    type="button"
                    class="queue-button"
                    onclick="completeTopic(${topic.id})"
                >
                    Complete
                </button>

            `;


            queueElement.appendChild(item);
        }
    );
}


/* =========================================================
   DIFFICULTY CLASS
   ========================================================= */

function getDifficultyClass(
    difficulty
) {

    const value =
        String(difficulty)
            .toLowerCase();


    if (value === "easy") {
        return "easy";
    }

    if (value === "hard") {
        return "hard";
    }

    return "medium";
}


/* =========================================================
   COMPLETE TOPIC
   ========================================================= */

function completeTopic(id) {

    const index =
        studyQueue.findIndex(
            function (topic) {

                return topic.id === id;
            }
        );


    if (index === -1) {
        return;
    }


    const topic =
        studyQueue[index];


    topic.completed = true;


    // Push completed topic into revision stack
    revisionStack.push({

        ...topic,

        revisionNumber: 1,

        nextRevision:
            calculateNextRevisionDate(1)
    });


    // Remove topic from queue
    studyQueue.splice(index, 1);


    plannerData.hoursStudied +=
        topic.duration / 60;


    plannerData.continuousSessions += 1;


    savePlannerData();

    updatePlannerDisplay();

    calculateAndDisplayFatigue();
}


/* =========================================================
   REVISION DATE
   ========================================================= */

function calculateNextRevisionDate(
    cycle
) {

    const date =
        new Date();


    const intervals = [
        1,
        3,
        7,
        14,
        30
    ];


    const days =
        intervals[
            Math.min(
                cycle - 1,
                intervals.length - 1
            )
        ];


    date.setDate(
        date.getDate() + days
    );


    return date.toISOString();
}


/* =========================================================
   FATIGUE INPUTS
   ========================================================= */

function setupFatigueInputs() {

    const inputs = [

        "hoursStudied",

        "continuousSessions",

        "difficultyLevel",

        "sleepHours",

        "breaksTaken",

        "mood"
    ];


    inputs.forEach(
        function (id) {

            const element =
                document.getElementById(id);


            if (!element) {
                return;
            }


            element.addEventListener(
                "input",
                updateFatigueFromForm
            );


            element.addEventListener(
                "change",
                updateFatigueFromForm
            );
        }
    );
}


/* =========================================================
   FATIGUE FROM FORM
   ========================================================= */

function updateFatigueFromForm() {

    const hours =
        getNumberValue(
            "hoursStudied",
            plannerData.hoursStudied
        );


    const sessions =
        getNumberValue(
            "continuousSessions",
            plannerData.continuousSessions
        );


    const difficulty =
        getNumberValue(
            "difficultyLevel",
            plannerData.difficulty
        );


    const sleep =
        getNumberValue(
            "sleepHours",
            plannerData.sleepHours
        );


    const breaks =
        getNumberValue(
            "breaksTaken",
            plannerData.breaks
        );


    const moodElement =
        document.getElementById(
            "mood"
        );


    plannerData.hoursStudied =
        hours;

    plannerData.continuousSessions =
        sessions;

    plannerData.difficulty =
        difficulty;

    plannerData.sleepHours =
        sleep;

    plannerData.breaks =
        breaks;


    if (moodElement) {

        plannerData.mood =
            moodElement.value;
    }


    calculateAndDisplayFatigue();
}


/* =========================================================
   NUMBER VALUE
   ========================================================= */

function getNumberValue(
    elementId,
    defaultValue
) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element) {
        return defaultValue;
    }


    const value =
        Number(element.value);


    if (Number.isNaN(value)) {
        return defaultValue;
    }


    return value;
}


/* =========================================================
   FATIGUE FORMULA
   =========================================================

   Fatigue Score =
   (H × 2)
   + (C × 1.5)
   + (D × 1)
   − (B × 2)
   − (S × 1.5)
   ========================================================= */

function calculateFatigue(
    hours,
    continuousSessions,
    difficulty,
    breaks,
    sleep
) {

    const score =
        (hours * 2) +
        (continuousSessions * 1.5) +
        (difficulty * 1) -
        (breaks * 2) -
        (sleep * 1.5);


    return Math.max(
        0,
        Number(score.toFixed(2))
    );
}


/* =========================================================
   FATIGUE LEVEL
   ========================================================= */

function getFatigueLevel(score) {

    if (score <= 5) {

        return "Normal";

    } else if (score <= 10) {

        return "Mild Fatigue";

    } else if (score <= 15) {

        return "High Fatigue";

    }

    return "Critical Fatigue";
}


/* =========================================================
   CALCULATE + DISPLAY FATIGUE
   ========================================================= */

function calculateAndDisplayFatigue() {

    const score =
        calculateFatigue(

            plannerData.hoursStudied,

            plannerData.continuousSessions,

            plannerData.difficulty,

            plannerData.breaks,

            plannerData.sleepHours
        );


    const level =
        getFatigueLevel(score);


    plannerData.fatigueScore =
        score;

    plannerData.fatigueLevel =
        level;


    displayFatigue(
        score,
        level
    );


    if (
        level === "High Fatigue" ||
        level === "Critical Fatigue" ||
        plannerData.mood === "Stressed"
    ) {

        activateHealthMaintenanceMode();
    }


    savePlannerData();
}


/* =========================================================
   DISPLAY FATIGUE
   ========================================================= */

function displayFatigue(
    score,
    level
) {

    const scoreElement =
        document.getElementById(
            "fatigueScore"
        );


    const levelElement =
        document.getElementById(
            "fatigueLevel"
        );


    const messageElement =
        document.getElementById(
            "fatigueMessage"
        );


    const meterElement =
        document.getElementById(
            "fatigueMeter"
        );


    if (scoreElement) {

        scoreElement.textContent =
            score.toFixed(1);
    }


    if (levelElement) {

        levelElement.textContent =
            level;
    }


    if (messageElement) {

        messageElement.textContent =
            getFatigueMessage(level);
    }


    if (meterElement) {

        const percentage =
            Math.min(
                (score / 20) * 100,
                100
            );


        meterElement.style.width =
            percentage + "%";
    }
}


/* =========================================================
   FATIGUE MESSAGE
   ========================================================= */

function getFatigueMessage(level) {

    switch (level) {

        case "Normal":
            return "Your study load looks balanced. Keep going.";

        case "Mild Fatigue":
            return "You may benefit from a few extra breaks.";

        case "High Fatigue":
            return "Your study load should be reduced and difficult topics moved.";

        case "Critical Fatigue":
            return "Health Maintenance Mode has been activated.";

        default:
            return "Keep monitoring your study and rest balance.";
    }
}


/* =========================================================
   HEALTH MAINTENANCE MODE
   ========================================================= */

function activateHealthMaintenanceMode() {

    const hardTopics =
        studyQueue.filter(
            function (topic) {

                return String(topic.difficulty)
                    .toLowerCase() === "hard";
            }
        );


    // Move hard topics to the end
    if (hardTopics.length > 0) {

        const remainingTopics =
            studyQueue.filter(
                function (topic) {

                    return String(topic.difficulty)
                        .toLowerCase() !== "hard";
                }
            );


        studyQueue =
            [
                ...remainingTopics,
                ...hardTopics
            ];
    }


    // Only allow first 1–2 light topics
    const lightTopics =
        studyQueue.filter(
            function (topic) {

                return String(topic.difficulty)
                    .toLowerCase() !== "hard";
            }
        );


    if (lightTopics.length > 2) {

        const allowed =
            lightTopics.slice(0, 2);


        const hardTopicsAgain =
            studyQueue.filter(
                function (topic) {

                    return String(topic.difficulty)
                        .toLowerCase() === "hard";
                }
            );


        studyQueue =
            [
                ...allowed,
                ...hardTopicsAgain
            ];
    }


    savePlannerData();

    updatePlannerDisplay();

    showHealthModeNotice();
}


/* =========================================================
   HEALTH MODE NOTICE
   ========================================================= */

function showHealthModeNotice() {

    const existing =
        document.getElementById(
            "healthModeNotice"
        );


    if (existing) {
        return;
    }


    const queue =
        document.getElementById(
            "studyQueue"
        );


    if (!queue) {
        return;
    }


    const notice =
        document.createElement("div");


    notice.id =
        "healthModeNotice";


    notice.className =
        "health-warning";


    notice.innerHTML = `

        <strong>
            Health Maintenance Mode Active
        </strong>

        <p>
            Your schedule has been adjusted.
            Heavy topics have been moved later,
            and today's study load has been reduced.
            Remember to take regular breaks.
        </p>

    `;


    queue.parentElement.insertBefore(
        notice,
        queue
    );
}


/* =========================================================
   ESCAPE HTML
   ========================================================= */

function escapeHTML(value) {

    return String(value)

        .replaceAll("&", "&amp;")

        .replaceAll("<", "&lt;")

        .replaceAll(">", "&gt;")

        .replaceAll('"', "&quot;")

        .replaceAll("'", "&#039;");
}


/* =========================================================
   PUBLIC FUNCTIONS
   ========================================================= */

window.addTopicFromForm =
    addTopicFromForm;

window.completeTopic =
    completeTopic;

window.calculateFatigue =
    calculateFatigue;

window.activateHealthMaintenanceMode =
    activateHealthMaintenanceMode;