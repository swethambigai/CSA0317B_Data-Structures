/* =========================================================
   SMART STUDY PLANNER
   DASHBOARD JAVASCRIPT
   ========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    initializeDashboard();
});


/* =========================================================
   INITIALIZE DASHBOARD
   ========================================================= */

function initializeDashboard() {

    updateDashboardDate();
    updateDashboardTime();
    loadDashboardData();
    setupDashboardButtons();

    // Update the displayed time every minute
    setInterval(updateDashboardTime, 60000);
}


/* =========================================================
   DATE
   ========================================================= */

function updateDashboardDate() {

    const dateElement = document.getElementById("dashboardDate");

    if (!dateElement) {
        return;
    }

    const today = new Date();

    const options = {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric"
    };

    dateElement.textContent = today.toLocaleDateString(
        "en-IN",
        options
    );
}


/* =========================================================
   TIME
   ========================================================= */

function updateDashboardTime() {

    const timeElement = document.getElementById("dashboardTime");

    if (!timeElement) {
        return;
    }

    const now = new Date();

    const options = {
        hour: "2-digit",
        minute: "2-digit"
    };

    timeElement.textContent = now.toLocaleTimeString(
        "en-IN",
        options
    );
}


/* =========================================================
   LOAD DASHBOARD DATA
   ========================================================= */

function loadDashboardData() {

    const savedData = localStorage.getItem(
        "smartStudyPlannerData"
    );

    if (!savedData) {
        return;
    }

    try {

        const data = JSON.parse(savedData);

        updateDashboardStatistics(data);
        updateFatigueDisplay(data);

    } catch (error) {

        console.error(
            "Unable to load dashboard data:",
            error
        );
    }
}


/* =========================================================
   DASHBOARD STATISTICS
   ========================================================= */

function updateDashboardStatistics(data) {

    const totalHoursElement =
        document.getElementById("totalStudyHours");

    const completedElement =
        document.getElementById("completedTopics");

    const pendingElement =
        document.getElementById("pendingTopics");

    const productivityElement =
        document.getElementById("productivityScore");


    if (totalHoursElement && data.totalHours !== undefined) {

        totalHoursElement.textContent =
            Number(data.totalHours).toFixed(1) + "h";
    }


    if (completedElement && data.completedTopics !== undefined) {

        completedElement.textContent =
            data.completedTopics;
    }


    if (pendingElement && data.pendingTopics !== undefined) {

        pendingElement.textContent =
            data.pendingTopics;
    }


    if (
        productivityElement &&
        data.productivityScore !== undefined
    ) {

        productivityElement.textContent =
            data.productivityScore + "%";
    }
}


/* =========================================================
   FATIGUE DISPLAY
   ========================================================= */

function updateFatigueDisplay(data) {

    if (data.fatigueScore === undefined) {
        return;
    }

    const score = Number(data.fatigueScore);

    const scoreElement =
        document.getElementById("fatigueScore");

    const levelElement =
        document.getElementById("fatigueLevel");

    const meterElement =
        document.getElementById("fatigueMeter");

    const messageElement =
        document.getElementById("fatigueMessage");


    if (scoreElement) {

        scoreElement.textContent =
            score.toFixed(1);
    }


    let level = "";
    let message = "";

    if (score <= 5) {

        level = "Normal";
        message =
            "Your current study load looks balanced.";

    } else if (score <= 10) {

        level = "Mild Fatigue";
        message =
            "Consider taking a few additional breaks.";

    } else if (score <= 15) {

        level = "High Fatigue";
        message =
            "Your study load should be reduced.";

    } else {

        level = "Critical Fatigue";
        message =
            "Health Maintenance Mode is recommended.";
    }


    if (levelElement) {

        levelElement.textContent =
            level;
    }


    if (messageElement) {

        messageElement.textContent =
            message;
    }


    if (meterElement) {

        let percentage =
            Math.min((score / 20) * 100, 100);

        meterElement.style.width =
            percentage + "%";
    }
}


/* =========================================================
   DASHBOARD BUTTONS
   ========================================================= */

function setupDashboardButtons() {

    const healthButton =
        document.getElementById("healthModeButton");

    if (healthButton) {

        healthButton.addEventListener(
            "click",
            function () {

                window.location.href =
                    "/health-mode";
            }
        );
    }


    const plannerButton =
        document.getElementById("plannerButton");

    if (plannerButton) {

        plannerButton.addEventListener(
            "click",
            function () {

                window.location.href =
                    "/planner";
            }
        );
    }
}


/* =========================================================
   COMPLETE STUDY SESSION
   ========================================================= */

function completeStudySession(topic) {

    let data =
        JSON.parse(
            localStorage.getItem(
                "smartStudyPlannerData"
            )
        ) || {};


    data.completedTopics =
        Number(data.completedTopics || 0) + 1;


    data.pendingTopics =
        Math.max(
            Number(data.pendingTopics || 0) - 1,
            0
        );


    localStorage.setItem(
        "smartStudyPlannerData",
        JSON.stringify(data)
    );


    loadDashboardData();
}


/* =========================================================
   PRODUCTIVITY SCORE
   ========================================================= */

function calculateProductivityScore(
    completedTopics,
    totalTopics,
    studyHours,
    targetHours
) {

    if (totalTopics <= 0 || targetHours <= 0) {
        return 0;
    }

    const completionScore =
        (completedTopics / totalTopics) * 50;

    const studyScore =
        Math.min(
            (studyHours / targetHours) * 50,
            50
        );

    return Math.round(
        completionScore + studyScore
    );
}