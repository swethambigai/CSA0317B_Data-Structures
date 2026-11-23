/* =========================================================
   SMART STUDY PLANNER
   ANALYTICS JAVASCRIPT
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    initializeAnalytics();
});


/* =========================================================
   INITIALIZE
   ========================================================= */

function initializeAnalytics() {

    loadAnalyticsData();

    calculateAnalytics();

    createStudyHoursChart();

    createFatigueChart();

    updateRevisionAnalytics();

    updateScheduleQuality();
}


/* =========================================================
   GET PLANNER DATA
   ========================================================= */

function getPlannerData() {

    const saved =
        localStorage.getItem(
            "smartStudyPlannerPlanner"
        );


    if (!saved) {

        return {

            studyQueue: [],

            revisionStack: [],

            plannerData: {}
        };
    }


    try {

        return JSON.parse(saved);

    } catch (error) {

        console.error(
            "Analytics data error:",
            error
        );


        return {

            studyQueue: [],

            revisionStack: [],

            plannerData: {}
        };
    }
}


/* =========================================================
   LOAD ANALYTICS
   ========================================================= */

function loadAnalyticsData() {

    // Prefer authoritative server statistics when available
    const serverStats = window.serverStatistics || null;

    if (serverStats) {
        updateElement("analyticsHours", (Number(serverStats.total_study_hours) || 0).toFixed(1) + "h");
        updateElement("analyticsFatigue", (Number(serverStats.average_fatigue) || 0).toFixed(1));
        updateElement("analyticsTopics", Number(serverStats.completed_topics) || 0);
        const prod = calculateProductivity(Number(serverStats.completed_topics) || 0, Number(serverStats.total_topics) || 0, Number(serverStats.total_study_hours) || 0);
        updateElement("analyticsProductivity", prod + "%");
        return;
    }

    // Fallback to planner localStorage data
    const data = getPlannerData();
    const planner = data.plannerData || {};

    const totalHours = Number(planner.hoursStudied || 0);
    const fatigueScore = Number(planner.fatigueScore || 0);
    const completed = Number(localStorage.getItem("completedTopics") || 0);
    const totalTopics = data.studyQueue.length + data.revisionStack.length + completed;
    const productivity = calculateProductivity(completed, totalTopics, totalHours);

    updateElement("analyticsHours", totalHours.toFixed(1) + "h");
    updateElement("analyticsFatigue", fatigueScore.toFixed(1));
    updateElement("analyticsTopics", totalTopics);
    updateElement("analyticsProductivity", productivity + "%");
}


/* =========================================================
   CALCULATE ANALYTICS
   ========================================================= */

function calculateAnalytics() {

    const data =
        getPlannerData();


    const planner =
        data.plannerData || {};


    const hours =
        Number(
            planner.hoursStudied || 0
        );


    const fatigue =
        Number(
            planner.fatigueScore || 0
        );


    updateElement(
        "currentStudyHours",
        hours.toFixed(1)
    );


    updateElement(
        "currentFatigue",
        fatigue.toFixed(1)
    );
}


/* =========================================================
   PRODUCTIVITY
   ========================================================= */

function calculateProductivity(
    completedTopics,
    totalTopics,
    studyHours
) {

    if (totalTopics === 0) {
        return 0;
    }


    const completionScore =
        (
            completedTopics /
            totalTopics
        ) * 70;


    const studyScore =
        Math.min(
            studyHours * 5,
            30
        );


    return Math.min(
        Math.round(
            completionScore +
            studyScore
        ),
        100
    );
}


/* =========================================================
   STUDY HOURS CHART
   ========================================================= */

function createStudyHoursChart() {

    const container =
        document.getElementById(
            "studyHoursChart"
        );


    if (!container) {
        return;
    }


    const stored =
        localStorage.getItem(
            "studyHistory"
        );


    let history = [];


    if (stored) {

        try {

            history =
                JSON.parse(stored);

        } catch (error) {

            history = [];
        }
    }


    // Use current data when history is empty
    if (history.length === 0) {

        const planner =
            getPlannerData()
                .plannerData || {};


        history = [
            {
                day: "Today",
                hours:
                    Number(
                        planner.hoursStudied || 0
                    )
            }
        ];
    }


    container.innerHTML = "";


    const chart =
        document.createElement("div");


    chart.className =
        "bar-chart";


    const maximum =
        Math.max(
            ...history.map(
                item =>
                    Number(item.hours) || 0
            ),
            1
        );


    history.slice(-7).forEach(
        function (item) {

            const bar =
                document.createElement("div");


            bar.className =
                "bar";


            const height =
                (
                    Number(item.hours) /
                    maximum
                ) * 180;


            bar.style.height =
                Math.max(
                    height,
                    10
                ) + "px";


            const label =
                document.createElement("span");


            label.className =
                "bar-label";


            label.textContent =
                item.day;


            bar.appendChild(label);

            chart.appendChild(bar);
        }
    );


    container.appendChild(chart);
}


/* =========================================================
   FATIGUE CHART
   ========================================================= */

function createFatigueChart() {

    const container =
        document.getElementById(
            "fatigueTrend"
        );


    if (!container) {
        return;
    }


    const stored =
        localStorage.getItem(
            "fatigueHistory"
        );


    let history = [];


    if (stored) {

        try {

            history =
                JSON.parse(stored);

        } catch (error) {

            history = [];
        }
    }


    if (history.length === 0) {

        const planner =
            getPlannerData()
                .plannerData || {};


        history = [
            {
                day: "Today",
                score:
                    Number(
                        planner.fatigueScore || 0
                    )
            }
        ];
    }


    container.innerHTML = "";


    history.slice(-7).forEach(
        function (item) {

            const row =
                document.createElement("div");


            row.className =
                "fatigue-day";


            const day =
                document.createElement("span");


            day.className =
                "fatigue-day-name";


            day.textContent =
                item.day;


            const bar =
                document.createElement("div");


            bar.className =
                "fatigue-bar";


            const fill =
                document.createElement("div");


            fill.className =
                "fatigue-bar-fill";


            const score =
                Number(
                    item.score || 0
                );


            fill.style.width =
                Math.min(
                    (score / 20) * 100,
                    100
                ) + "%";


            bar.appendChild(fill);


            const value =
                document.createElement("span");


            value.className =
                "fatigue-value";


            value.textContent =
                score.toFixed(1);


            row.appendChild(day);

            row.appendChild(bar);

            row.appendChild(value);


            container.appendChild(row);
        }
    );
}


/* =========================================================
   REVISION ANALYTICS
   ========================================================= */

function updateRevisionAnalytics() {

    const data =
        getPlannerData();


    const revisionStack =
        data.revisionStack || [];


    const total =
        revisionStack.length;


    const completed =
        revisionStack.filter(
            topic =>
                topic.revisionNumber > 1
        ).length;


    const dueToday =
        revisionStack.filter(
            topic => {

                if (!topic.nextRevision) {
                    return false;
                }


                const revisionDate =
                    new Date(
                        topic.nextRevision
                    );


                const today =
                    new Date();


                return (
                    revisionDate.toDateString() ===
                    today.toDateString()
                );
            }
        ).length;


    updateElement(
        "revisionTotal",
        total
    );


    updateElement(
        "revisionCompleted",
        completed
    );


    updateElement(
        "revisionDue",
        dueToday
    );
}


/* =========================================================
   SCHEDULE QUALITY
   ========================================================= */

function updateScheduleQuality() {

    const data =
        getPlannerData();


    const queue =
        data.studyQueue || [];


    const planner =
        data.plannerData || {};


    const hours =
        Number(
            planner.hoursStudied || 0
        );


    const fatigue =
        Number(
            planner.fatigueScore || 0
        );


    const overloaded =
        hours > 8 ||
        fatigue > 15;


    const balanced =
        hours >= 2 &&
        hours <= 6 &&
        fatigue <= 10;


    const overloadedElement =
        document.getElementById(
            "overloadedStatus"
        );


    const balancedElement =
        document.getElementById(
            "balancedStatus"
        );


    const pendingElement =
        document.getElementById(
            "pendingStatus"
        );


    if (overloadedElement) {

        overloadedElement.textContent =
            overloaded
                ? "Needs Attention"
                : "Good";
    }


    if (balancedElement) {

        balancedElement.textContent =
            balanced
                ? "Balanced"
                : "Review";
    }


    if (pendingElement) {

        pendingElement.textContent =
            queue.length +
            " topics";
    }
}


/* =========================================================
   SAVE TODAY'S HISTORY
   ========================================================= */

function saveAnalyticsHistory() {

    const data =
        getPlannerData();


    const planner =
        data.plannerData || {};


    const today =
        new Date();


    const day =
        today.toLocaleDateString(
            "en-IN",
            {
                weekday: "short"
            }
        );


    saveHistoryItem(
        "studyHistory",
        {
            day: day,
            hours:
                Number(
                    planner.hoursStudied || 0
                )
        }
    );


    saveHistoryItem(
        "fatigueHistory",
        {
            day: day,
            score:
                Number(
                    planner.fatigueScore || 0
                )
        }
    );
}


/* =========================================================
   SAVE HISTORY ITEM
   ========================================================= */

function saveHistoryItem(
    storageKey,
    newItem
) {

    let history = [];


    const stored =
        localStorage.getItem(
            storageKey
        );


    if (stored) {

        try {

            history =
                JSON.parse(stored);

        } catch (error) {

            history = [];
        }
    }


    history.push(newItem);


    history =
        history.slice(-7);


    localStorage.setItem(
        storageKey,
        JSON.stringify(history)
    );
}


/* =========================================================
   UPDATE ELEMENT
   ========================================================= */

function updateElement(
    id,
    value
) {

    const element =
        document.getElementById(id);


    if (element) {

        element.textContent =
            value;
    }
}


/* =========================================================
   INITIALIZE HISTORY
   ========================================================= */

saveAnalyticsHistory();


/* =========================================================
   PUBLIC FUNCTIONS
   ========================================================= */

window.calculateProductivity =
    calculateProductivity;

window.saveAnalyticsHistory =
    saveAnalyticsHistory;